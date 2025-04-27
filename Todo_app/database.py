from sqlmodel import create_engine, Session

# Criação do ponto de conexão com a base de dados Postgres. echo = True permite que seja imprimidas todas as instruções SQL que estão acontecer
engine = create_engine("sqlite:///db.db", echo=True)


def get_session():
    with Session(engine) as session:
        yield session  # yield é um gerador e retorna a session parando a execução desta função mas mantendo o seu estado (utilização da session) até a resposta ser enviada e fechar a session
