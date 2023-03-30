import sys
sys.path.append("../TRACK_BITCOIN")
import config
import requests
import logging
import time
import config
import telegram
import asyncio

logger = logging.getLogger(__name__)

BITCOIN_URL = "https://economia.awesomeapi.com.br/last/BTC-BRL"
DOLAR_URL = "https://economia.awesomeapi.com.br/last/USD-BRL"
LIBRA_URL = "https://economia.awesomeapi.com.br/last/GBP-BRL"

BOT_TOKEN = config.TOKEN
CHAT_ID = config.CHAT_ID

def get_price() -> dict:
    try:
        logger.info(f" Buscando valor do Bitcoin...")
        response1 = requests.get(BITCOIN_URL)
        logger.info(f" Done!")
        data = response1.json()
        logger.info(f" Buscando valor do Dolar...")
        response2 = requests.get(DOLAR_URL)
        logger.info(f" Done!")
        data2 = response2.json()
        logger.info(f" Buscando valor da Libra...")
        response3 = requests.get(LIBRA_URL)
        logger.info(f" Done!")
        data3= response3.json()
    except:
        logger.error(f"Falha ao buscar dados")
        return {}
    if response1.status_code == 200 and response2.status_code == 200 and response3.status_code == 200:
        return {'bitcoin': data['BTCBRL']['bid'], 'dolar': data2['USDBRL']['bid'], 
                'libra': data3['GBPBRL']['bid']}
    return {}

async def run():
    bot = telegram.Bot(BOT_TOKEN)
    async with bot:
        while True:
            price = get_price()
            if price:
                msg = f"Preço de compra do Bitcoin é: R${price['bitcoin']},00\nPreço de compra do dolar é: R${price['dolar']},00\nPreço de compra da libra é: R${price['libra']},00"
                await bot.send_message(text=msg, chat_id = CHAT_ID)
            time.sleep(60*10)

if __name__ == "__main__":
    asyncio.run(run())
