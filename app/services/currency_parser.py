import httpx
from bs4 import BeautifulSoup
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.crud import create_currency, get_currency


async def get_currency_data(db: AsyncSession):
    url = "https://www.cbr.ru/currency_base/daily/"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        rows = soup.find('table', {'class': 'data'}).find_all('tr')[1:]

        for row in rows:
            columns = row.find_all('td')
            if len(columns) < 5:
                continue

            code = columns[1].text.strip()
            currency = columns[3].text.strip()
            rate = float(columns[4].text.replace(',', '.').strip())

            existing_currency = await get_currency(db, code)
            if existing_currency:
                existing_currency.rate = rate
                await db.commit()
                await db.refresh(existing_currency)
            else:
                await create_currency(db, code, currency, rate)

        return {"message": "Currency data has been updated."}