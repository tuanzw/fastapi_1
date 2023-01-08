from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, insert, delete
from sqlalchemy.orm import joinedload
from models import *


async def create_hero(session: AsyncSession, heroCreate: HeroCreate):
    stmt = insert(Hero).values(heroCreate.dict())
    result = await session.execute(stmt)
    # await session.commit()
    print(result.inserted_primary_key)
    (last_record_id,) = result.inserted_primary_key
    hero = HeroRead(**heroCreate.dict(), id=last_record_id)
    return hero


async def list_hero(session: AsyncSession, skip: int, limit: int):
    stmt = select(Hero).offset(skip).limit(limit)
    result = await session.execute(stmt)
    return result.scalars().all()


async def get_hero_by_id(session: AsyncSession, id: int):
    stmt = select(Hero).where(Hero.id == id).options(joinedload(Hero.team))
    result = await session.execute(stmt)
    return result.scalar()


async def patch_hero(session: AsyncSession, id: int, hero: HeroUpdate):
    hero_data = hero.dict(exclude_unset=True)
    stmt = update(Hero).where(Hero.id == id).values(hero_data)
    await session.execute(stmt)
    # await session.commit()
    return await get_hero_by_id(session, id)


async def delete_hero(session: AsyncSession, id: int):
    stmt = delete(Hero).where(Hero.id == id)
    result = await session.execute(stmt)
    # await session.commit()
    return result.rowcount


async def create_team(session: AsyncSession, team_create: TeamCreate):
    stmt = insert(Team).values(team_create.dict())
    result = await session.execute(stmt)
    # await session.commit()
    (last_record_id,) = result.inserted_primary_key
    team = TeamRead(**team_create.dict(), id=last_record_id)
    return team


async def list_team(session: AsyncSession, skip: int, limit: int):
    stmt = select(Team).offset(skip).limit(limit)
    result = await session.execute(stmt)
    return result.scalars().all()


async def get_team_by_id(session: AsyncSession, id: int):
    stmt = select(Team).where(Team.id == id).options(joinedload(Team.heroes))
    result = await session.execute(stmt)
    return result.scalar()


async def patch_team(session: AsyncSession, id: int, team_update: TeamUpdate):
    team_data = team_update.dict(exclude_unset=True)
    stmt = update(Team).where(Team.id == id).values(team_data)
    await session.execute(stmt)
    # await session.commit()
    return await get_team_by_id(session, id)


async def delete_team(session: AsyncSession, id: int):
    stmt = delete(Team).where(Team.id == id)
    result = await session.execute(stmt)
    # await session.commit()
    return result.rowcount
