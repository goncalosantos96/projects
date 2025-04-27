from http import HTTPStatus


def test_get_task_by_id(client):

    # Request POST para criar uma nova task
    client.post("/tasks/", json={"title": "Cozinha", "description": "Fazer o jantar"})

    # Request POST para criar uma nova task
    client.post(
        "/tasks/",
        json={"title": "Escola", "description": "Estudar para o teste de Matemática"},
    )

    # Request GET para obter task com id == 2
    response = client.get("/tasks/2")

    # Verificação que a operação para obter uma task foi bem sucedida
    assert response.status_code == HTTPStatus.OK

    # Verificação se foi obtida a task esperada
    assert response.json() == {
        "id": 2,
        "title": "Escola",
        "description": "Estudar para o teste de Matemática",
        "status": "pending",
    }


def test_get_tasks(client):

    # Request POST para criar uma nova task
    client.post("/tasks/", json={"title": "Cozinha", "description": "Fazer o jantar"})

    # Request POST para criar uma nova task
    client.post(
        "/tasks/",
        json={"title": "Escola", "description": "Estudar para o teste de Matemática"},
    )

    # Request GET para obter as tasks
    response = client.get("/tasks/")

    # Verificação que as operação para obter as tasks foi bem sucedida
    assert response.status_code == HTTPStatus.OK

    # Verificação se foram obtidas as tasks
    assert response.json() == [
        {
            "id": 1,
            "title": "Cozinha",
            "description": "Fazer o jantar",
            "status": "pending",
        },
        {
            "id": 2,
            "title": "Escola",
            "description": "Estudar para o teste de Matemática",
            "status": "pending",
        },
    ]
