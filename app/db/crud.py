from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Currency


async def get_currencies(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Currency).offset(skip).limit(limit))
    return result.scalars().all()


async def get_currency(db: AsyncSession, currency_id: int):
    result = await db.execute(select(Currency).filter(Currency.id == currency_id))
    return result.scalars().first()


async def create_currency(db: AsyncSession, code: str, currency: str, rate: float):
    db_currency = Currency(code=code, currency=currency, rate=rate)
    db.add(db_currency)
    await db.commit()
    await db.refresh(db_currency)
    return db_currency


async def update_currency(db: AsyncSession, currency_id: int, rate: float):
    result = await db.execute(select(Currency).filter(Currency.id == currency_id))
    db_currency = result.scalars().first()
    if db_currency:
        db_currency.rate = rate
        await db.commit()
        await db.refresh(db_currency)
        return db_currency
    return None


async def delete_currency(db: AsyncSession, currency_id: int):
    result = await db.execute(select(Currency).filter(Currency.id == currency_id))
    db_currency = result.scalars().first()
    if db_currency:
        await db.delete(db_currency)
        await db.commit()
        return {"message": f"Currency {currency_id} deleted successfully"}
    return None