# WasteWise backend - main file
# This is the entry point of our server. Everything starts here.

from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from . import models  # noqa: F401  (importing it lets SQLAlchemy know about our tables)
from .database import Base, engine, get_db

# Create all the tables in PostgreSQL if they do not exist yet.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="WasteWise API",
    description="Backend for the WasteWise waste management system",
)


@app.get("/")
def home():
    return {"message": "Welcome to WasteWise API"}


@app.get("/health")
def health():
    return {"status": "ok"}


# Tests that Python can really talk to PostgreSQL.
# Depends(get_db) means: "FastAPI, please open a database session for me".
@app.get("/db-test")
def db_test(db: Session = Depends(get_db)):
    version = db.execute(text("SELECT version()")).scalar()
    tables = db.execute(
        text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name")
    ).scalars().all()
    return {"database": "connected", "postgres_version": version, "tables": tables}
