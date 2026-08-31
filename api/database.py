from collections.abc import Generator

from sqlalchemy.orm import DeclarativeBase, create_engine, sessionmaker

DATABASE_URL = "postgresql+psycopg://postgres:password@localhost/mydb"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


def get_db() -> Generator:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
