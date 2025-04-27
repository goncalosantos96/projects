import pytest

from Todo_app.repository import TaskRepository
from Todo_app.models import Task
from fastapi import HTTPException
from http import HTTPStatus


def test_repository_add(session):

    # Criação de repositorio
    repo = TaskRepository(session)

    # Criação de task
    task = Task(title="Cozinha", description="Lavar os pratos")

    # Adicionar task ao repositorio
    task_added = repo.add(task)

    # Persistir dados na base de dados em memoria
    session.commit()

    # Atualização dos dados da task_added (atribuição de id pela base de dados)
    session.refresh(task_added)

    # verificação se foi atribuido id (sendo atribuido é porque adicionou na base de dados)
    assert task_added.id == 1


def test_repository_add_exception_id(session):

    # Criação de repositorio
    repo = TaskRepository(session)

    # Criação de task
    task = Task(id=-1, title="Cozinha", description="Lavar os pratos")

    # Captura a excepção caso seja levantada (caso contrário o teste falha se não for levantada a excepção esperada)
    with pytest.raises(HTTPException) as exception_msg:
        repo.add(task)

    # verificação se foi levantada uma HTTException para o id não válido
    assert exception_msg.value.status_code == HTTPStatus.BAD_REQUEST
    assert exception_msg.value.detail == "ID provided is not allowed!"


def test_repository_add_exception_status(session):

    # Criação de repositorio
    repo = TaskRepository(session)

    # Criação de task
    task = Task(title="Cozinha", description="Lavar os pratos", status="doing")

    # Captura a excepção caso seja levantada (caso contrário o teste falha se não for levantada a excepção esperada)
    with pytest.raises(HTTPException) as exception_msg:
        repo.add(task)

    # verificação se foi levantada uma HTTException para o status inválido
    assert exception_msg.value.status_code == HTTPStatus.BAD_REQUEST
    assert exception_msg.value.detail == "The value must be 'pending' or 'completed'!"


def test_repository_add_exception_existing_id(session):

    # Criação de repositorio
    repo = TaskRepository(session)

    # Criação de task1
    task1 = Task(id=1, title="Cozinha", description="Lavar os pratos")

    # Criação de task2
    task2 = Task(id=1, title="Escola", description="Fazer os trabalhos da escola")

    # Adicionar task1 ao repositorio
    repo.add(task1)

    # Persistencia dos dados task1 na base de dados
    session.commit()

    # Captura a excepção caso seja levantada (caso contrário o teste falha se não for levantada a excepção esperada)
    with pytest.raises(HTTPException) as exception_msg:
        repo.add(task2)

    # verificação se foi levantada uma HTTException para o id que já existe
    assert exception_msg.value.status_code == HTTPStatus.BAD_REQUEST
    assert exception_msg.value.detail == "ID provided already exists!"


def test_repository_get_task_by_id(session):

    # Criaçao de repositorio
    repo = TaskRepository(session)

    # Criação de task1
    task1 = Task(title="Cozinha", description="Lavar os pratos")

    # Criaçao de task2
    task2 = Task(title="Escola", description="Fazer os trabalhos da escola")

    # Adicionar task1 ao repositorio
    repo.add(task1)

    # #Adicionar task2 ao repositorio
    repo.add(task2)

    # Persistir dados na base de dados em memoria
    session.commit()

    # Obtenção da task com o id == 1
    result1 = repo.get_task_by_id(1)

    # Obtenção da task com o id == 2
    result2 = repo.get_task_by_id(2)

    # Verificação se foi obtida a task com o id == 1
    assert result1.id == 1

    # Verificação se foi obtida a task com o id == 2
    assert result2.id == 2


def test_repository_get_tasks(session):

    # Criaçao de repositorio
    repo = TaskRepository(session)

    # Criação de task1
    task1 = Task(title="Cozinha", description="Lavar os pratos")

    # Criaçao de task2
    task2 = Task(title="Escola", description="Fazer os trabalhos da escola")

    # #Adicionar task1 ao repositorio
    repo.add(task1)

    # #Adicionar task2 ao repositorio
    repo.add(task2)

    # Persistir dados na base de dados em memoria
    session.commit()

    # Obtenção das tasks
    result = repo.get_tasks()

    # Verificação se foi obtida a lista toda de tasks
    assert result[0].id == 1
    assert result[1].id == 2


def test_repository_delete(session):
    # Criaçao de repositorio
    repo = TaskRepository(session)

    # Criação de task1
    task1 = Task(title="Cozinha", description="Lavar os pratos")

    # Criaçao de task2
    task2 = Task(title="Escola", description="Fazer os trabalhos da escola")

    # Criação de task3
    task3 = Task(title="Compras", description="Ir ao shopping fazer compras")

    # Adicionar task1 ao repositorio
    repo.add(task1)

    # Adicionar task2 ao repositorio
    repo.add(task2)

    # Adicionar task3 ao repositorio
    repo.add(task3)

    # Persistir dados na base de dados em memoria
    session.commit()

    # Atualização dos dados da task1 (atribuição de id pela base de dados)
    session.refresh(task1)

    # Atualização dos dados da task2 (atribuição de id pela base de dados)
    session.refresh(task2)

    # Atualização dos dados da task3 (atribuição de id pela base de dados)
    session.refresh(task3)

    # Remoção da task com o id == 2
    repo.delete(task2.id)

    # Persistir a eliminação dos dados na base de dados em memoria
    session.commit()

    # Obtenção das tasks
    result = repo.get_tasks()

    assert result[0].id == task1.id
    assert result[1].id == task3.id


def test_repository_update(session):
    # Criação de repositorio
    repo = TaskRepository(session)

    # Criação de task
    task = Task(title="Cozinha", description="Lavar os pratos")

    # Adicionar task ao repositorio
    repo.add(task)

    # Persistir dados na base de dados em memoria
    session.commit()

    # Atualização dos stauts da task_added
    result_updated = repo.update_task_status(1, "completed")

    # Persistir dados na base de dados em memoria
    session.commit()

    # verificação se foi atribuido id (sendo atribuido é porque adicionou na base de dados)
    assert result_updated.status == "completed"


def test_repository_update_exception(session):
    # Criaçao de repositorio
    repo = TaskRepository(session)

    # Criação de task
    task = Task(title="Cozinha", description="Lavar os pratos")

    # Adicionar task ao repositorio
    repo.add(task)

    # Persistir dados na base de dados em memoria
    session.commit()

    # Captura a excepção caso seja levantada (caso contrário o teste falha se não for levantada a excepção esperada)
    with pytest.raises(HTTPException) as exception_msg1:
        # Foi pedido para atualizar o estado das task com id == 2 (Não existe)
        repo.update_task_status(2, "completed")

    # Captura a excepção caso seja levantada (caso contrário o teste falha se não for levantada a excepção esperada)
    with pytest.raises(HTTPException) as exception_msg2:
        # Foi pedido para atualizar o estado das task com id == 1 (Existe) mas com um estado que não aceite
        repo.update_task_status(1, "doing")

    assert exception_msg1.value.status_code == HTTPStatus.NOT_FOUND
    assert exception_msg2.value.status_code == HTTPStatus.BAD_REQUEST


def test_repository_get_by_id_exception(session):
    # Criaçao de repositorio
    repo = TaskRepository(session)

    # Criação de task
    task = Task(title="Cozinha", description="Lavar os pratos")

    # Adicionar task ao repositorio
    repo.add(task)

    # Persistir dados na base de dados em memoria
    session.commit()

    # Captura a excepção caso seja levantada (caso contrário o teste falha se não for levantada a excepção esperada)
    with pytest.raises(HTTPException) as exception_msg:
        # Foi pedido para atualizar o estado das task com id == 2 (Não existe)
        repo.get_task_by_id(2)

    assert exception_msg.value.status_code == HTTPStatus.NOT_FOUND


def test_repository_delete_exception(session):
    # Criaçao de repositorio
    repo = TaskRepository(session)

    # Criação de task
    task = Task(title="Cozinha", description="Lavar os pratos")

    # Adicionar task ao repositorio
    repo.add(task)

    # Persistir dados na base de dados em memoria
    session.commit()

    # Captura a excepção caso seja levantada (caso contrário o teste falha se não for levantada a excepção esperada)
    with pytest.raises(HTTPException) as exception_msg:
        # Foi pedido para atualizar o estado das task com id == 2 (Não existe)
        repo.delete(2)

    assert exception_msg.value.status_code == HTTPStatus.NOT_FOUND
