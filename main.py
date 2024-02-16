import uvicorn
from typing import List, Optional
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI, Depends, Query, HTTPException, Request, Header, Form

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


from database import create_db_and_tables, async_session
from models import *
import services as _services

app = FastAPI()


templates = Jinja2Templates(directory="templates")


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


@app.get("/index/", response_class=HTMLResponse)
def index(request: Request, hx_request: Optional[str] = Header(None)):
    title = "FastAPI with HTMX"
    heroes = [
        {
            "name": "Tuan.Nguyen",
            "status": 1,
            "age": 41,
            "date": "12/21/2021",
            "description": "Lorem ipsum dolor sit amet. Eos doloremque accusamus qui inventore animi hic reprehenderit voluptas ut animi odio a mollitia libero quo magnam galisum id dolores beatae",
            "color": "green",
        },
        {
            "name": "Chris.Booth",
            "status": 2,
            "age": 57,
            "date": "09/18/2022",
            "description": "Lorem ipsum dolor sit amet. Eos doloremque accusamus qui inventore animi hic reprehenderit voluptas ut animi odio a mollitia libero quo magnam galisum id dolores beatae",
            "color": "yellow",
        },
        {
            "name": "Patrick.Stephen",
            "status": 0,
            "age": 62,
            "date": "09/12/2021",
            "description": "Lorem ipsum dolor sit amet. Eos doloremque accusamus qui inventore animi hic reprehenderit voluptas ut animi odio a mollitia libero quo magnam galisum id dolores beatae",
            "color": "gray",
        },
    ]
    context = {"request": request, "title": title, "heroes": heroes}
    if hx_request:
        return templates.TemplateResponse("hero.html", context)
    return templates.TemplateResponse("index.html", context)


@app.get("/gate_entries", response_model=List[GateEntryRead])
async def gate_entries(
    session: AsyncSession = Depends(get_session),
    skip: int = 0,
    limit: int = Query(default=10),
):
    return await _services.list_gate_entry(session=session, skip=skip, limit=limit)


@app.get("/gate_entries/{uuid}", response_model=GateEntryRead)
async def gateentry_by_id(*, session: AsyncSession = Depends(get_session), uuid: str):
    db_gateentry = await _services.get_gateentry_by_id(session=session, uuid=uuid)
    if not db_gateentry:
        raise HTTPException(status_code=404, detail="Not found!")

    return db_gateentry


@app.patch("/gate_entries/{uuid}", response_model=GateEntryRead)
async def patch_gateentry(
    *,
    session: AsyncSession = Depends(get_session),
    uuid: str,
    gateentry_update: GateEntryUpdate,
):
    db_gateentry = await _services.patch_gate_entry(
        session=session, uuid=uuid, gateentry_update=gateentry_update
    )
    if not db_gateentry:
        raise HTTPException(status_code=404, detail="Not found")
    return db_gateentry


@app.post("/gate_entries/", response_model=GateEntryRead)
async def create_gate_entry(
    *, session: AsyncSession = Depends(get_session), gate_entry_create: GateEntryCreate
):
    return await _services.create_gate_entry(
        session=session, gate_entry_create=gate_entry_create
    )


@app.get("/gateentries/", response_class=HTMLResponse)
async def gateentries(
    request: Request,
    hx_request: Optional[str] = Header(None),
    session: AsyncSession = Depends(get_session),
):
    title = "Gate Entry HTMX"
    gateentries = await _services.list_gate_entry_by_date(
        session=session, wdate=date.today(), filter_txt=None
    )
    context = {"request": request, "title": title, "gateentries": gateentries}
    if hx_request:
        return templates.TemplateResponse("gateentry.html", context)
    return templates.TemplateResponse("gateentryhtmx.html", context)


@app.post("/search_gateentries/", response_class=HTMLResponse)
async def search_gateentries(
    request: Request,
    hx_request: Optional[str] = Header(None),
    session: AsyncSession = Depends(get_session),
    search: str = Form(None),
):
    title = "Gate Entry HTMX"
    gateentries = await _services.list_gate_entry_by_date(
        session=session, wdate=date.today(), filter_txt=search
    )
    context = {"request": request, "title": title, "gateentries": gateentries}
    return templates.TemplateResponse("gateentry.html", context)


@app.patch("/gate_entry_cf/{uuid}", response_class=HTMLResponse)
async def gate_entry_cf(
    *, request: Request, session: AsyncSession = Depends(get_session), uuid: str
):
    data = {"status": 9}
    gateentry_update = GateEntryUpdate.parse_obj(data)
    gateentry = await _services.patch_gate_entry(
        session=session, uuid=uuid, gateentry_update=gateentry_update
    )
    context = {"request": request, "gateentries": [gateentry]}
    return templates.TemplateResponse("gateentry.html", context)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
