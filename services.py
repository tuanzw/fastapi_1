from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, update, insert, delete, func, col
from sqlalchemy.orm import joinedload

# from sqlalchemy import func
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


async def create_gate_entry(session: AsyncSession, gate_entry_create: GateEntryCreate):
    stmt = insert(GateEntry).values(gate_entry_create.dict())
    result = await session.execute(stmt)
    # await session.commit()
    (created_uuid,) = result.inserted_primary_key
    gate_entry = GateEntryRead(**gate_entry_create.dict(), uuid=created_uuid)
    return gate_entry


async def list_gate_entry(session: AsyncSession, skip: int, limit: int):
    stmt = select(GateEntry).offset(skip).limit(limit)
    result = await session.execute(stmt)
    return result.scalars().all()


async def list_gate_entry_by_date(session: AsyncSession, wdate: date, filter_txt: str):
    stmt = select(GateEntry)
    # if wdate:
    #     stmt = stmt.where(func.DATE(GateEntry.register_dstamp) == wdate)

    if filter_txt:
        # stmt = stmt.where(GateEntry.vehicle_license_plate.like(f"%{filter_txt}%"))
        stmt = stmt.where(col(GateEntry.vehicle_license_plate).contains(filter_txt))

    result = await session.execute(stmt)
    return result.scalars().all()


async def get_gateentry_by_id(session: AsyncSession, uuid: str):
    stmt = select(GateEntry).where(GateEntry.uuid == uuid)
    result = await session.execute(stmt)
    return result.scalar()


async def patch_gate_entry(
    session: AsyncSession, uuid: str, gateentry_update: GateEntryUpdate
):
    gateentry_data = gateentry_update.dict(exclude_unset=True)
    stmt = update(GateEntry).where(GateEntry.uuid == uuid).values(gateentry_data)
    await session.execute(stmt)
    return await get_gateentry_by_id(session, uuid)
