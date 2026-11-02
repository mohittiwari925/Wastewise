# database.py - connects our Python code to PostgreSQL

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Read the secret settings (like the password) from the .env file.
# We do this so passwords are never written inside the code.
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise RuntimeError("DATABASE_URL is missing. Create a .env file (see .env.example).")

# The engine is the actual connection to PostgreSQL.
engine = create_engine(DATABASE_URL)

# A session is one "conversation" with the database (read, add, save).
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Every table class in models.py inherits from this Base.
Base = declarative_base()


# FastAPI will call this for each request: open a session, use it, then close it.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
