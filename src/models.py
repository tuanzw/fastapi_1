from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


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
