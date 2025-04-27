from sqlmodel import Session
from Todo_app.unit_of_work import Unit_of_Work
from Todo_app.repository import Task, TaskRepository


class Queries:

    def __init__(self, session: Session):
        self.session = session

    def read_task_by_id(self, task_id: id):
        # Criação da unit of work
        unit_of_work = Unit_of_Work(self.session, TaskRepository(self.session))

        # Obtenção da task com o task_id providenciado
        task = unit_of_work.task_repo.get_task_by_id(task_id)

        return task

    def read_tasks(self) -> list[Task]:
        # Criação da unit of work
        unit_of_work = Unit_of_Work(self.session, TaskRepository(self.session))

        # Obtenção de todas as tasks
        tasks = unit_of_work.task_repo.get_tasks()
        return tasks
