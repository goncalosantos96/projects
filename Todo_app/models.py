from sqlmodel import SQLModel, Field
from typing import Optional


# Criação da classe Task. table = True faz com que a classe seja tratada como um tabela na base de dados
class Task(SQLModel, table=True):
    # Optional faz com que o atributo id não seja passado. O default = None faz com que este valor (devido a ser uma chave-primaria) seja atribuido pela base de dados
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    status: str = "pending"


# Esta classe é tratada como um schema
class Status_Update(SQLModel):
    status: str
