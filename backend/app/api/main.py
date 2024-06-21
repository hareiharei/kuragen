from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud
from .routes import members

router = APIRouter()
router.include_router(members.router, prefix="/members", tags=["members"])