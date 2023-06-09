import sys
sys.path.append("../TRACK_BITCOIN")
from config import settings
import requests
import logging
import time
import telegram
import asyncio
import json

logger = logging.getLogger(__name__)

BITCOIN_URL = settings.BITCOIN_URL
DOLAR_URL = settings.DOLAR_URL
LIBRA_URL = settings.LIBRA_URL

BOT_TOKEN = settings.TOKEN
CHAT_ID = settings.CHAT_ID

def get_price() -> dict:
    """
    Pega o valor do bid das três moedas. Se alguma falhar, 
    ele interrompe e não manda nada
    """
    try:
        logger.info(f" Buscando valor do Bitcoin...")
        response1: requests.Response = requests.get(BITCOIN_URL)
        logger.info(f" Done!")
        data: json = response1.json()
        logger.info(f" Buscando valor do Dolar...")
        response2: requests.Response = requests.get(DOLAR_URL)
        logger.info(f" Done!")
        data2: json = response2.json()
        logger.info(f" Buscando valor da Libra...")
        response3: requests.Response = requests.get(LIBRA_URL)
        logger.info(f" Done!")
        data3: json = response3.json()
    except:
        logger.error(f"Falha ao buscar dados")
        return {}
    if response1.status_code == 200 and response2.status_code == 200 and response3.status_code == 200:
        return {'bitcoin': data['BTCBRL']['bid'], 'dolar': data2['USDBRL']['bid'], 
                'libra': data3['GBPBRL']['bid']}
    return {}

async def run():
    bot = telegram.Bot(BOT_TOKEN)
    price: float = 0
    async with bot:
        while True:
            price = get_price()
            if price:
                msg = f"Preço de compra do Bitcoin é: R${price['bitcoin']},00\nPreço de compra do dolar é: R${price['dolar']},00\nPreço de compra da libra é: R${price['libra']},00"
                await bot.send_message(text=msg, chat_id = CHAT_ID)
            time.sleep(60*10)

if __name__ == "__main__":
    asyncio.run(run())
