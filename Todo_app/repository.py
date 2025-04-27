from sqlmodel import Session, select
from Todo_app.models import Task
from http import HTTPStatus
from fastapi import HTTPException


class TaskRepository:

    def __init__(self, session: Session):
        # Repositorio recebe a session onde se vai executar os diferentes operações
        self.session = session

    def add(self, task: Task) -> Task:
        # Criação de query para verificar se existe alguma task com este id
        query = select(Task).where(Task.id == task.id)

        # Obtenção do objecto a verificar
        result = self.session.scalar(query)

        # Verificação se foi providenciado o id para adicionar
        if task.id:
            # Verificação se o id providenciado é inválido
            if task.id < 1:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail="ID provided is not allowed!",
                )

        # Verificação se o id providenciado já existe
        if result:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail="ID provided already exists!"
            )

        # Verificação se existe o new_status está dentro da opções aceitaveis
        if (
            task.status.lower().strip() != "pending"
            and task.status.lower().strip() != "completed"
        ):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="The value must be 'pending' or 'completed'!",
            )

        # adiciona task enviada no repositório da sessão
        self.session.add(task)
        return task

    def get_task_by_id(self, task_id: id) -> Task:

        # Criação de query para obter resultado da task que queremos consultar
        query = select(Task).where(Task.id == task_id)

        # Obtenção do objecto a consultar
        result = self.session.scalar(query)

        # Verificação se existe a task com o task_id providenciado
        if not result:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="ID provided not found!"
            )

        return result

    def get_tasks(self) -> list[Task]:

        # Criação de query para obter resultado com todas as tasks
        query = select(Task)

        # Obtenção de todos os objectos Task
        results = self.session.exec(query).all()

        print(results)

        return results

    def delete(self, task_id: int) -> Task:

        # Criação de query para obter resultado da task que pretendemos eliminar
        query = select(Task).where(Task.id == task_id)

        # Obtenção do objecto a remover
        result = self.session.scalar(query)

        # Verificação se existe a task com o task_id providenciado
        if not result:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="ID provided not found!"
            )

        # Remoção do resultado
        self.session.delete(result)

        return result

    def update_task_status(self, task_id: int, new_status: str) -> Task:

        # Criação de query para obter resultado da task que pretendemos alterar
        query = select(Task).where(Task.id == task_id)

        # Obtenção do objecto a alterar
        result = self.session.scalar(query)

        # Verificação se existe a task com o task_id providenciado
        if not result:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="ID provided not found!"
            )

        # Verificação se existe o new_status está dentro da opções aceitaveis
        if (
            new_status.lower().strip() != "pending"
            and new_status.lower().strip() != "completed"
        ):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="The value must be 'pending' or 'completed'!",
            )

        # Atualização do objecto com o new_status
        result.status = new_status

        return result
