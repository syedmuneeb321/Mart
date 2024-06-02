from sqlmodel import SQLModel,Session,create_engine


connection_string = "sqlite:///mart.db"
engine = create_engine(connection_string,echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        return session 