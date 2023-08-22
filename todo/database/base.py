# import os
# from typing import Generator

# from sqlalchemy import create_engine
# from sqlalchemy.orm import declarative_base, sessionmaker, Session

# from todo.config import config


# Base = declarative_base()


# def create_db_path():
#     BASE_DIR = os.path.dirname(os.path.abspath(__name__))
#     db_path = os.path.join(BASE_DIR, "todo", "database", "DB")
#     if not os.path.exists(db_path):
#         os.makedirs(db_path)


# # create_db_path()

# engine = create_engine(
#     config.db_url.get_secret_value(),
#     connect_args={"check_same_thread": False},
#     echo=True,
# )


# def get_db() -> Generator:
#     session: Session = SessionLocal()
#     try:
#         yield session
#     finally:
#         session.close()


# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
