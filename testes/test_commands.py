from http import HTTPStatus


def test_command_create_task(client):

    # Request POST para criar uma nova task
    response = client.post(
        "/tasks/", json={"title": "Cozinha", "description": "Fazer o jantar"}
    )

    # Verificação que o a task foi criada na base de dados
    assert response.status_code == HTTPStatus.CREATED

    # Verificação que a task foi criada como seria esperado
    assert response.json() == {
        "id": 1,
        "title": "Cozinha",
        "description": "Fazer o jantar",
        "status": "pending",
    }


def test_command_updtate_task(client):

    # Request POST para criar uma nova task para poder ser modificada
    client.post("/tasks/", json={"title": "Cozinha", "description": "Fazer o jantar"})

    # Request PATCH para modificar parcialmente (status) a task
    response = client.patch("/tasks/1", json={"status": "completed"})

    # Verificação que a task foi modificada
    assert response.status_code == HTTPStatus.OK

    # Verificação que a task foi modificada como seria esperado
    assert response.json() == {
        "id": 1,
        "title": "Cozinha",
        "description": "Fazer o jantar",
        "status": "completed",
    }


def test_command_delete_task(client):

    # Request POST para criar uma nova task para poder ser eliminada
    client.post("/tasks/", json={"title": "Cozinha", "description": "Fazer o jantar"})

    # Request DELETE para eliminar task
    response = client.delete("/tasks/1")

    # Verificação que a task foi eliminada
    assert response.status_code == HTTPStatus.OK

    # Verificação que a task eliminada era a esperada
    assert response.json() == {
        "id": 1,
        "title": "Cozinha",
        "description": "Fazer o jantar",
        "status": "pending",
    }
