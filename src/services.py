from sqlmodel import Session
from .models import *


def create_hero(session: Session, heroCreate: HeroCreate):
    db_hero = Hero.from_orm(heroCreate)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


def list_hero(session: Session, skip: int, limit: int):
    return session.query(Hero).offset(offset=skip).limit(limit=limit).all()


def get_hero_by_id(session: Session, id: int):
    return session.get(entity=Hero, ident=id)


def update_hero_by_id(session: Session, db_hero: Hero, hero: HeroUpdate):

    hero_data = hero.dict(exclude_unset=True)
    for key, val in hero_data.items():
        setattr(db_hero, key, val)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


def patch_hero(session: Session, id: int, hero: HeroUpdate):
    db_hero = get_hero_by_id(session=session, id=id)
    if db_hero:
        hero_data = hero.dict(exclude_unset=True)
        for key, val in hero_data.items():
            setattr(db_hero, key, val)
        session.add(db_hero)
        session.commit()
        session.refresh(db_hero)
    return db_hero


def create_team(session: Session, team_create: TeamCreate):
    db_team = Team.from_orm(team_create)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team


def list_team(session: Session, skip: int, limit: int):
    return session.query(Team).offset(skip).limit(limit).all()


def get_team_by_id(session: Session, id: int):
    return session.get(Team, id)

def patch_team(session: Session, id: int, team_update:TeamUpdate):
    db_team = get_team_by_id(session, id)
    if db_team:
        team_data = team_update.dict(exclude_unset=True)
        for key, val in team_data.items():
            setattr(db_team, key, val)
        session.add(db_team)
        session.commit()
        session.refresh(db_team)
        
    return db_team
