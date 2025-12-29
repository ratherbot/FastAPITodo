from pydantic import BaseModel


class CurrencyBase(BaseModel):
    code: str
    currency: str
    rate: float

class CurrencyCreate(CurrencyBase):
    pass

class Currency(CurrencyBase):
    id: int

    class Config:
        from_attributes = True