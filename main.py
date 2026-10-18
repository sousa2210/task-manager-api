from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Response

from database import get_connection, initialize_database
from schemas import TaskCreate

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


@app.post("/tasks", status_code=201)
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


@app.get("/tasks")
def list_tasks():
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT * FROM tasks ORDER BY id"
        ).fetchall()

        return [task_to_dict(row) for row in rows]


@app.get("/tasks/{task_id}")
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


@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: TaskCreate):
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
