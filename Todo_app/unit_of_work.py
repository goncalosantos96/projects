from sqlmodel import Session
from Todo_app.repository import TaskRepository
from Todo_app.repository import Task


class Unit_of_Work:

    def __init__(self, session: Session, task_repo: TaskRepository):
        self.session = session
        self.task_repo = task_repo

    def commit(self):
        # Persiste os dados do repositorio da sessão na base de dados
        self.session.commit()

    def refresh(self, task: Task):
        # O refresh permite que a task adiciona na base de dados devolva o objecto atualizado (nomeadamente o id que é atribuido pela base de dados)
        self.session.refresh(task)
