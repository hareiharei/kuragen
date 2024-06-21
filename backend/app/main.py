from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Sessioin

from . import crud, models, schemas
from .database import SessionLocal, engine
from .api.main import router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()