from fastapi import FastAPI, WebSocket, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.db import crud, models, database
from app.db.models import create_tables
from app.nats.publisher import publish_unique_message
from app.schemas import Currency, CurrencyCreate
from app.ws.socket import websocket_endpoint
from app.tasks.background_task import run_background_task
import asyncio

app = FastAPI()


@app.on_event("startup")
async def startup():
    await create_tables()
    asyncio.create_task(run_background_task())


@app.websocket("/ws/items")
async def ws_items(websocket: WebSocket):
    await websocket_endpoint(websocket)


@app.get("/items", response_model=list[Currency])
async def get_items(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    return await crud.get_currencies(db, skip, limit)


@app.get("/items/{currency_id}", response_model=Currency)
async def get_item(currency_id: int, db: Session = Depends(database.get_db)):
    currency = await crud.get_currency(db, currency_id)
    if currency is None:
        raise HTTPException(
            status_code=404,
            detail=f"Currency with id {currency_id} not found"
        )
    return currency


@app.post("/items", response_model=Currency)
async def create_item(currency: CurrencyCreate, db: Session = Depends(database.get_db)):
    return await crud.create_currency(db, currency.code, currency.currency, currency.rate)


@app.patch("/items/{currency_id}", response_model=Currency)
async def update_item(currency_id: int, rate: float, db: Session = Depends(database.get_db)):
    return await crud.update_currency(db, currency_id, rate)


@app.delete("/items/{currency_id}", response_model=Currency)
async def delete_item(currency_id: int, db: Session = Depends(database.get_db)):
    return await crud.delete_currency(db, currency_id)

@app.get("/tasks/run")
async def run_task(background_tasks: BackgroundTasks):
    background_tasks.add_task(run_background_task)
    await publish_unique_message("currency.updates")
    return {"message": "Background task has been started!"}