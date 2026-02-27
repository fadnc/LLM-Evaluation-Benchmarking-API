import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL",
                         "postgresql://user:password@localhost:5432/llm_eval")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocomit=False, autoflush=False, bind=engine)

Base = declarative_base()