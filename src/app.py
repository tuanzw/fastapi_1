from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI, Depends, Query, HTTPException
from .database import create_db_and_tables, async_session
from .models import *
from . import services as _services

app = FastAPI()


@app.on_event("startup")
async def startup():
    await create_db_and_tables()


# Dependency
async def get_session():
    async with async_session() as session:
        async with session.begin():
            yield session


@app.post("/heros/", response_model=HeroRead)
async def create_hero(
    *, session: AsyncSession = Depends(get_session), hero: HeroCreate
):
    return await _services.create_hero(session=session, heroCreate=hero)


@app.get("/heros/", response_model=List[HeroRead])
async def get_heros(
    *,
    session: AsyncSession = Depends(get_session),
    skip: int = 0,
    limit: int = Query(default=10, lte=100),
):
    return await _services.list_hero(session=session, skip=skip, limit=limit)


@app.get("/heros/{hero_id}", response_model=HeroReadWithTeam)
async def get_hero(*, session: AsyncSession = Depends(get_session), hero_id: int):
    db_hero = await _services.get_hero_by_id(session=session, id=hero_id)
    if db_hero is None:
        raise HTTPException(status_code=404, detail="Hero not found")

    return db_hero


@app.patch("/heros/{hero_id}", response_model=HeroRead)
async def update_hero(
    *, session: AsyncSession = Depends(get_session), hero_id: int, hero: HeroUpdate
):
    db_hero = await _services.patch_hero(session=session, id=hero_id, hero=hero)
    if not db_hero:
        raise HTTPException(status_code=404, detail="Hero not found")

    return db_hero


@app.delete("/heros/{hero_id}")
async def delete_hero(*, session: AsyncSession = Depends(get_session), hero_id: int):
    delete_count = await _services.delete_hero(session=session, id=hero_id)
    return {"message": f"Deleted {delete_count} hero(es)"}


@app.post("/teams/", response_model=TeamRead)
async def create_team(
    *, session: AsyncSession = Depends(get_session), team: TeamCreate
):
    return await _services.create_team(session=session, team_create=team)


@app.get("/teams/", response_model=List[TeamRead])
async def get_team(
    *,
    session: AsyncSession = Depends(get_session),
    skip: int = 0,
    limit: int = Query(default=10, lte=10),
):
    return await _services.list_team(session=session, skip=skip, limit=limit)


@app.get("/teams/{team_id}", response_model=TeamReadwithHeroes)
async def get_team(*, session: AsyncSession = Depends(get_session), team_id: int):
    db_team = await _services.get_team_by_id(session, team_id)
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")

    return db_team


@app.patch("/teams/{team_id}", response_model=TeamRead)
async def update_team(
    *,
    session: AsyncSession = Depends(get_session),
    team_id: int,
    team_update: TeamUpdate,
):
    db_team = await _services.patch_team(session, team_id, team_update)
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")

    return db_team


@app.delete("/teams/{team_id}")
async def delete_team(*, session: AsyncSession = Depends(get_session), team_id: int):
    delete_count = await _services.delete_team(session=session, id=team_id)
    return {"message": f"Deleted {delete_count} team(s)"}
