import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

TOKEN = os.getenv('TOKEN')

WEBHOOK_PATH = f"/main/{TOKEN}"
APP_URL = os.getenv('APP_URL')
WEBHOOK_URL = APP_URL + WEBHOOK_PATH

ORDERS_CHAT_ID = -1001721955838
QA_CHAT_ID = -1001824115877
