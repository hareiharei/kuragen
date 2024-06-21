from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Time, Datetime
from sqlalchemy.orm import relationship

from .database import Base

class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)    # ハッシュ化する
    last_name = Column(String, nullable=False)   # カタカナ
    first_name = Column(String, nullable=False)  # カタカナ
    generation = Column(Integer, nullable=False)


class RoleType(Base):
    __tablename__ = "roletypes"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    is_staff = Column(Boolean, nullable=False)

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    roletype_id = Column(Integer, ForeignKey("role"), nullable=False)
    
class Concert(Base):
    __tablename__ = "concerts"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    practice_starts_on = Column(Date, nullable=False)
    practice_ends_on = Column(Date, nullable=False)
    held_on = Column(Date, nullable=False)

class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True)
    concert_id = Column(Integer, ForeignKey("concerts.id"), nullable=False)
    title = Column(String, nullable=False)
    author = Column(String)

class RideNumber(Base):
    __tablename__ = "ridenumbers"

    id = Column(Integer, primary_key=True)
    song_id = Column(Integer, ForeignKey("songs.id"), nullable=False)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    part = Column(String, nullable=False)
    is_leader = Column(Boolean, nullable=False)

class Period(Base):
    __tablename__ = "periods"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    starts_at = Column(Time, nullable=False)
    ends_at = Column(Time, nullable=False)

class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True)
    period_id = Column(Integer, ForeignKey("periods.id"), nullable=False)
    song_id = Column(Integer, ForeignKey("songs.id"), nullable=False)
    held_on = Column(Date, nullable=False)
    room_name = Column(String, nullable=False)
    room_type = Column(String, nullable=False)
    practice_type = Column(String, nullable=False)
    created_at = Column(Datetime, nullable=False)
    updated_at = Column(Datetime)

class Absense(Base):
    __tablename__ = "absenses"

    id = Column(Integer, primary_key=True)
    schedule_id = Column(Integer, ForeignKey("schedules.id"), nullable=False)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(Datetime, nullable=False)
    updated_at = Column(Datetime)

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True)
    schedule_id = Column(Integer, ForeignKey("notes.id"), nullable=False)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(Datetime, nullable=False)
    updated_at = Column(Datetime)

'''

参考にしたサイト:
https://fastapi.tiangolo.com/tutorial/sql-databases/

relationship追加する必要あり

'''