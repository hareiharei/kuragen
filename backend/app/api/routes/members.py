from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ... import schemas, crud

router = APIRouter()

@router.post("/", response_model=schemas.Member)
def create_member(member: schemas.MemberCreate, db: Session = Depends(get_db)):
    db_member = crud.read.member.get_member_by_email(db, email=member.email)
    if db_member:
        raise HTTPException(status_code=400, detail="Emailが既に登録されています")
    return crud.create.member.create_member(db=db, member=member)