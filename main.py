
from fastapi import FastAPI

app = FastAPI(
    title="Task Manager API",
    description="API para gerenciamento de tarefas",
    version="0.1.0",
)


@app.get("/")
def read_root():
    return {
        "message": "Task Manager API está funcionando!",
        "status": "online",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
