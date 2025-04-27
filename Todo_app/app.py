from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, Session
from Todo_app.database import engine, get_session
from Todo_app.models import Task, Status_Update
from Todo_app.commands import Commands
from Todo_app.queries import Queries
from pprint import pprint
from http import HTTPStatus

# Criação de instância da aplicação FastAPI
app = FastAPI()

# Criação de todas as tabelas (que herdam de SQLModel - herdam funcionalidades do pydantic com do sqlalchemy) através dos metadados na base de dados Postgres
SQLModel.metadata.create_all(engine)


@app.post("/tasks/", status_code=HTTPStatus.CREATED, response_model=Task)
def create_task(
    task: Task, session: Session = Depends(get_session)
):  # Usa-se o Depends para informar o FastAPI que necessitamos desta dependencia para obter a session

    # Criação de uma instância Commands (comando realiza operações que alteram o estado da base de dados)
    command = Commands(session)

    # Criação de uma nova tarefa -> o método model_dump converte um modelo pydantic (Task) em um dicionario
    task_add = command.create_task(Task(**task.model_dump()))

    # resposta enviado ao cliente
    return task_add


@app.delete("/tasks/{task_id}", status_code=HTTPStatus.OK, response_model=Task)
def delete_task(task_id: int, session: Session = Depends(get_session)):

    # Criação de uma instância Commands (comando realiza operações que alteram o estado da base de dados)
    command = Commands(session)

    # Remoção da task com task_id
    task_rm = command.delete_task(task_id)

    # resposta enviado ao cliente
    return task_rm


@app.get("/tasks/{task_id}", status_code=HTTPStatus.OK, response_model=Task)
def get_task_by_id(task_id: int, session: Session = Depends(get_session)):

    # Criação de instancia Queries
    query = Queries(session)

    # Obtenção da task com o task_id
    result = query.read_task_by_id(task_id)

    return result


@app.get("/tasks/", status_code=HTTPStatus.OK, response_model=list[Task])
def get_tasks(session: Session = Depends(get_session)):

    # Criação de instancia Queries
    query = Queries(session)

    # Obtenção das tasks na base de dados
    tasks = query.read_tasks()

    pprint(tasks)

    return tasks


@app.patch("/tasks/{task_id}", status_code=HTTPStatus.OK, response_model=Task)
def update_task(
    task_id: int, new_status: Status_Update, session: Session = Depends(get_session)
):
    # Criação de uma instância Commands (comando realiza operações que alteram o estado da base de dados)
    command = Commands(session)

    # Alteração do status da task na base de dados
    updated_task = command.update_status(task_id, new_status.status)

    return updated_task
