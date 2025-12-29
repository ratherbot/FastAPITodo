from sqlalchemy.orm import Session
from app.db.models import Currency

def get_currencies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Currency).offset(skip).limit(limit).all()

def get_currency(db: Session, currency_id: int):
    return db.query(Currency).filter(Currency.id == currency_id).first()

def create_currency(db: Session, code: str, currency: str, rate: float):
    db_currency = Currency(code=code, currency=currency, rate=rate)
    db.add(db_currency)
    db.commit()
    db.refresh(db_currency)
    return db_currency

def update_currency(db: Session, currency_id: int, rate: float):
    db_currency = db.query(Currency).filter(Currency.code == currency_id).first()
    if db_currency:
        db_currency.rate = rate
        db.commit()
        db.refresh(db_currency)
        return db_currency
    return None

def delete_currency(db: Session, currency_id: int):
    db_currency = db.query(Currency).filter(Currency.code == currency_id).first()
    if db_currency:
        db.delete(db_currency)
        db.commit()
        return {"message": f"Currency {currency_id} deleted successfully"}
    return None