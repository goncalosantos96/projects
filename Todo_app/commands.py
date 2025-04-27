from sqlmodel import Session
from Todo_app.unit_of_work import Unit_of_Work
from Todo_app.repository import Task, TaskRepository


class Commands:

    def __init__(self, session: Session):
        self.session = session

    def create_task(self, task: Task) -> Task:
        # Criação da unit of work
        unit_work = Unit_of_Work(self.session, TaskRepository(self.session))

        # Adição de task no repositorio
        unit_work.task_repo.add(task)

        # Persistencia dos dados do repositorio na base de dados
        unit_work.commit()

        # Atualização dos dados providenciados (obtenção do id atribuido pela base de dados)
        unit_work.refresh(task)

        return task

    def update_status(self, task_id: int, new_status: str) -> Task:
        # Criação da unit of work
        unit_of_work = Unit_of_Work(self.session, TaskRepository(self.session))

        # Alteração do status da task com o task_id providenciado
        updated_task = unit_of_work.task_repo.update_task_status(task_id, new_status)

        # Persistencia da alteraçao na base de dados
        unit_of_work.commit()

        # Obtenção da task atualizada
        unit_of_work.refresh(updated_task)

        return updated_task

    def delete_task(self, task_id: int) -> Task:
        # Criação da unit of work
        unit_of_work = Unit_of_Work(self.session, TaskRepository(self.session))

        # Remoção de task no repositorio
        task = unit_of_work.task_repo.delete(task_id)

        # Eliminação dos dados do repositorio na base de dados
        unit_of_work.commit()

        return task
