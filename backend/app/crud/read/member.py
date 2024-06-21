from sqlalchemy.orm import Session
from ... import models, schemas

def get_member_by_email(db: Session, email: str):
    # db_member = db.execute(
    #     """
    #     SELECT * FROM members
    #     WHERE email = :email
    #     """,
    #     {'email': email}
    # )
    # return db_member

    return db.query(models.Member).filter(models.Member.email == email).first()
    