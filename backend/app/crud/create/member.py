from sqlalchemy.orm import Session
from ... import models, schemas

def create_member(db: Session, member: schemas.MemberCreate):
    db.execute(
        "INSERT INTO members (email, password, last_name, first_name, generation) \
         VALUES (:email, :password, :last_name, :first_name, :generation)",
        {
            'email': member.email,
            'password': member.password,
            'last_name': member.last_name,
            'first_name': member.first_name,
            'generation': member.generation
        }
    )
    db.commit()