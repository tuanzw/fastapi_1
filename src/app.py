from typing import List
from sqlmodel import Session
from fastapi import FastAPI, Depends, Query, HTTPException
from .database import create_db_and_tables, engine
from .models import *
from . import services as _services

app = FastAPI()


@app.on_event("startup")
def startup():
    create_db_and_tables()


# Dependency
def get_session():
    with Session(engine) as session:
        yield session


@app.post("/heros/", response_model=HeroRead)
def create_hero(*, session: Session = Depends(get_session), hero: HeroCreate):
    return _services.create_hero(session=session, heroCreate=hero)


@app.get("/heros/", response_model=List[HeroCreate])
def get_heros(
    *,
    session: Session = Depends(get_session),
    skip: int = 0,
    limit: int = Query(default=10, lte=100)
):
    return _services.list_hero(session=session, skip=skip, limit=limit)


@app.get("/heros/{hero_id}", response_model=HeroReadWithTeam)
def get_hero(*, session: Session = Depends(get_session), hero_id: int):
    db_hero = _services.get_hero_by_id(session=session, id=hero_id)
    if db_hero is None:
        raise HTTPException(status_code=404, detail="Hero not found")

    return db_hero


# @app.patch("/heros/{hero_id}", response_model=HeroRead)
# def update_hero(
#     *, session: Session = Depends(get_session), hero_id: int, hero: HeroUpdate
# ):
#     db_hero = get_hero_by_id(session=session, id=hero_id)
#     if not db_hero:
#         raise HTTPException(status_code=404, detail="Hero not found")

#     return update_hero_by_id(session=session, db_hero=db_hero, hero=hero)


@app.patch("/heros/{hero_id}", response_model=HeroRead)
def update_hero(
    *, session: Session = Depends(get_session), hero_id: int, hero: HeroUpdate
):
    db_hero = _services.patch_hero(session=session, id=hero_id, hero=hero)
    if not db_hero:
        raise HTTPException(status_code=404, detail="Hero not found")

    return db_hero


@app.post("/teams/", response_model=TeamRead)
def create_team(*, session: Session = Depends(get_session), team: TeamCreate):
    return _services.create_team(session=session, team_create=team)


@app.get("/teams/", response_model=List[TeamRead])
def get_team(
    *,
    session: Session = Depends(get_session),
    skip: int = 0,
    limit: int = Query(default=10, lte=10)
):
    return _services.list_team(session=session, skip=skip, limit=limit)


@app.get("/teams/{team_id}", response_model=TeamReadwithHeroes)
def get_team(*, session: Session = Depends(get_session), team_id: int):
    db_team = _services.get_team_by_id(session, team_id)
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")

    return db_team


@app.patch("/teams/{team_id}", response_model=TeamRead)
def update_team(
    *, session: Session = Depends(get_session), team_id: int, team_update: TeamUpdate
):
    db_team = _services.patch_team(session, team_id, team_update)
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")

    return db_team
