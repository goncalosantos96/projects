import pytest
from sqlmodel import create_engine, Session, SQLModel
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from Todo_app.app import app, get_session


# Criação da fixture de session - As fixtures servem para preparar recursos antes de rodar os testes sem ter que os escrever em todos eles
@pytest.fixture
def session():
    # Criação de conexão a base de dados SQLite em memória, ou seja é criada do zero quando um teste começa
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # Criação da tabela através dos metadados
    SQLModel.metadata.create_all(engine)

    # Gerenciador de contexto da session
    with Session(engine) as session:
        # yield é um gerador e retorna a session parando a execução desta função mas mantendo o seu estado (utilização da session)
        yield session


@pytest.fixture
def client(session):

    # get_session_override retorna a fixture session - ou seja a session que é criada com a conexão da base de dados em memoria
    def get_session_override():
        yield session

    # Gerenciador de contexto onde é criado um client (simula requisições HTTP)
    with TestClient(app) as client:
        # Enquanto neste bloco (durante utilização de client) for pedido o get_session este é substituido pelo get_session_override
        app.dependency_overrides[get_session] = get_session_override

        # gerador que retorna o estado de client
        yield client

    # Acabando o teste limpa-se os overrides e fica com as dependencias habituais
    app.dependency_overrides.clear()
