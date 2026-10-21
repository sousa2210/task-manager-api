from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Query, Response

from database import get_connection, initialize_database
from schemas import TaskCreate, TaskUpdate, TaskResponse, TaskPartialUpdate

@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    yield


app = FastAPI(
    title="Task Manager API",
    description="API para gerenciamento de tarefas",
    version="0.4.0",
    lifespan=lifespan,
)



def task_to_dict(row):
    task = dict(row)
    task["completed"] = bool(task["completed"])
    return task




@app.get("/")
def read_root():
    return {
        "message": "Task Manager API está funcionando!",
        "status": "online",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/tasks", status_code=201, response_model=TaskResponse)
def create_task(task: TaskCreate):
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO tasks (title, description, completed)
            VALUES (?, ?, ?)
            """,
            (task.title, task.description, int(task.completed)),
        )

        row = connection.execute(
            "SELECT * FROM tasks WHERE id = ?",
            (cursor.lastrowid,),
        ).fetchone()

        return task_to_dict(row)





@app.get("/tasks", response_model=list[TaskResponse])
def list_tasks(
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    completed: bool | None = Query(default=None),
    search: str | None = Query(default=None, min_length=1, max_length=100),
):
    query = "SELECT * FROM tasks"
    conditions = []
    parameters = []

    if completed is not None:
        conditions.append("completed = ?")
        parameters.append(int(completed))

    if search is not None:
        conditions.append("title LIKE ?")
        parameters.append(f"%{search}%")

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY id LIMIT ? OFFSET ?"
    parameters.extend([limit, offset])

    with get_connection() as connection:
        rows = connection.execute(
            query,
            parameters,
        ).fetchall()

        return [task_to_dict(row) for row in rows]


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM tasks WHERE id = ?",
            (task_id,),
        ).fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Tarefa não encontrada",
            )

        return task_to_dict(row)


@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, updated_task: TaskUpdate):
    with get_connection() as connection:
        cursor = connection.execute(
            """
            UPDATE tasks
            SET title = ?, description = ?, completed = ?
            WHERE id = ?
            """,
            (
                updated_task.title,
                updated_task.description,
                int(updated_task.completed),
                task_id,
            ),
        )

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Tarefa não encontrada",
            )

        row = connection.execute(
            "SELECT * FROM tasks WHERE id = ?",
            (task_id,),
        ).fetchone()

        return task_to_dict(row)


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    with get_connection() as connection:
        cursor = connection.execute(
            "DELETE FROM tasks WHERE id = ?",
            (task_id,),
        )

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Tarefa não encontrada",
            )

    return Response(status_code=204)


@app.patch("/tasks/{task_id}", response_model=TaskResponse)
def partial_update_task(task_id: int, updated_fields: TaskPartialUpdate):
    changes = updated_fields.model_dump(exclude_unset=True)

    if not changes:
        raise HTTPException(
            status_code=400,
            detail="Envie pelo menos um campo para atualizar.",
        )

    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM tasks WHERE id = ?",
            (task_id,),
        ).fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Tarefa não encontrada",
            )


        values = []
        for field, value in changes.items():
            if field == "completed":
                value = int(value)

            values.append(value)

        set_clause = ", ".join(
            f"{field} = ?" for field in changes
        )

        connection.execute(
            f"UPDATE tasks SET {set_clause} WHERE id = ?",
            (*values, task_id),
        )

        updated_row = connection.execute(
            "SELECT * FROM tasks WHERE id = ?",
            (task_id,),
        ).fetchone()

        return task_to_dict(updated_row)
