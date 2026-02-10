from sqlalchemy import create_engine
from sqlalchemy import sessionmaker, declarative_base

DB_URL = "sqlite:///./taskflow.db"
engine = create_engine(DB_URL,connect_args={"check_same_thread":false})

SessionLocal = sessionmaker(autocommit=false,autoflush=false,bind=engine)
Base = declarative_base