from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
import uuid as uuid_pgk
from datetime import datetime


class GateEntryBase(SQLModel):
    site_id: int = Field(index=True)  # 0(Chutex) 1(ICD1)
    status: Optional[int] = Field(default=0, index=True)  # 0(Released) 9(Completed)
    vehicle_license_plate: str = Field(index=True, max_length=9)
    driver_id: Optional[str] = Field(default=None, max_length=12)
    register_dstamp: Optional[datetime] = Field(default_factory=datetime.now)
    entry_dstamp: Optional[datetime] = Field(default_factory=datetime.now)
    linein_dstamp: Optional[datetime] = Field(default=None)
    plan_entry_time: Optional[str] = Field(default=None, max_length=4)
    route_id: Optional[int] = Field(default=None)
    phone_no: Optional[str] = Field(default=None, max_length=15)


class GateEntry(GateEntryBase, table=True):
    __tablename__ = "gate_entry"
    uuid: uuid_pgk.UUID = Field(
        default_factory=uuid_pgk.uuid4, primary_key=True, index=True, nullable=False
    )


class GateEntryRead(GateEntryBase):
    uuid: uuid_pgk.UUID


class GateEntryCreate(GateEntryBase):
    pass


class GateEntryUpdate(GateEntryBase):
    site_id: Optional[int]
    status: int
    vehicle_license_plate: Optional[str]
    driver_id: Optional[str]
    entry_dstamp: Optional[datetime] = Field(default_factory=datetime.now)
    linein_dstamp: Optional[datetime]
    plan_entry_time: Optional[str]
    route_id: Optional[int]
    phone_no: Optional[str]


class HeroBase(SQLModel):
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)
    team_id: Optional[int] = Field(default=None, foreign_key="team.id")


class Hero(HeroBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    team: Optional["Team"] = Relationship(back_populates="heroes")


class HeroRead(HeroBase):
    id: int


class HeroCreate(HeroBase):
    pass


class HeroUpdate(HeroBase):
    name: Optional[str] = Field(default=None)
    secret_name: Optional[str] = Field(default=None)
    age: Optional[int] = Field(default=None)
    team_id: Optional[int] = Field(default=None)


class TeamBase(SQLModel):
    name: str = Field(index=True)
    headquarters: str


class Team(TeamBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    heroes: List["Hero"] = Relationship(back_populates="team")


class TeamCreate(TeamBase):
    pass


class TeamRead(TeamBase):
    id: int


class TeamUpdate(TeamBase):
    name: Optional[str] = Field(default=None)
    headquarters: Optional[str] = Field(default=None)


class HeroReadWithTeam(HeroRead):
    team: Optional[TeamRead] = None


class TeamReadwithHeroes(TeamRead):
    heroes: List[HeroRead] = []
