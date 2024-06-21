from sqlalchemy.orm import Session
from ... import models, schemas

def create_member(db: Session, creating_member: schemas.MemberCreate):
    # メンバーを作成
    # db.execute(
    #     """
    #     INSERT INTO members
    #     (email, password, last_name, first_name, generation)
    #     VALUES
    #     (:email, :password, :last_name, :first_name, :generation)
    #     """,
    #     {
    #         'email': creating_member.email,
    #         'password': creating_member.password,
    #         'last_name': creating_member.last_name,
    #         'first_name': creating_member.first_name,
    #         'generation': creating_member.generation
    #     }
    # )
    db_member = models.Member.model_validate(creating_member)
    db.commit()
    db.refresh(db_member)
    return db_member

    # 新しく作成されたメンバーを取得
    # result = db.execute(
    #     """
    #     "SELECT * FROM members 
    #      WHERE email = :email"
    #     """,
    #     {'email': member.email}
    # )

    # return result.fetchone()


# 参考にしたサイト：
# https://fastapi.tiangolo.com/tutorial/sql-databases/#__tabbed_1_1
# https://github.com/tiangolo/full-stack-fastapi-template/blob/master/backend/app/crud.py
