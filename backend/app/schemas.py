from pydantic import BaseModel
from datetime import date, datetime, time

class MemberBase(BaseModel):
    email: str
    password: str
    last_name: str
    first_name: str
    generation: int

class Member(MemberBase):
    id: int

    class Config:
        orm_mode = True

class MemberCreate(MemberBase):
    pass

class RoleTypeBase(BaseModel):
    title: str
    is_staff: bool

class RoleType(RoleTypeBase):
    id: int

class Role(BaseModel):
    id: int
    member_id: int
    roletype_id: int

    class Config:
        orm_mode = True
    
class ConcertBase(BaseModel):
    title: str
    practice_starts_on: date
    practice_ends_on: date
    held_on: date

class Concert(ConcertBase):
    id: int

    class Config:
        orm_mode = True

class SongBase(BaseModel):
    title: str
    author: str | None = None

class Song(SongBase):
    id: int
    concert_id: int

    class Config:
        orm_mode = True

class RideNumberBase(BaseModel):
    part: str
    is_leader: bool

class RideNumber(RideNumberBase):
    id: int
    song_id: int
    member_id: int

    class Config:
        orm_mode = True

class PeriodBase(BaseModel):
    title: str
    starts_at: time
    ends_at: time

class Period(PeriodBase):
    id: int

    class Config:
        orm_mode = True

class ScheduleBase(BaseModel):
    held_on: date
    room_name: str
    room_type: str
    practice_type: str
    created_at: datetime
    updated_at: datetime

class Schedule(ScheduleBase):
    id: int
    period_id: int
    song_id: int

    class Config:
        orm_mode = True

class AbsenseBase(BaseModel):
    content: str
    created_at: datetime
    updated_at: datetime

class Absense(AbsenseBase):
    id: int
    schedule_id: int
    member_id: int

    class Config:
        orm_mode = True