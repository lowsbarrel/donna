import os
from dotenv import main

main.load_dotenv()

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENAI_KEY = os.environ.get("OPENAI_KEY")
ELEVENLABS_KEY = os.environ.get("ELEVENLABS_KEY")
DATABASE_HOST = os.environ.get("DATABASE_HOST")
DATABASE_USERNAME = os.environ.get("DATABASE_USERNAME")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
DATABASE = os.environ.get("DATABASE")
WEBHOOK_HOST= os.environ.get("WEBHOOK_LISTEN")
WEBHOOK_PORT= os.environ.get("WEBHOOK_PORT")
SERVER_NAME= os.environ.get("SERVER_NAME")
BASE_WEBHOOK_URL = os.environ.get("BASE_WEBHOOK_URL")
WEBHOOK_PATH = os.environ.get("WEBHOOK_PATH")
SSL_CERT_PATH= os.environ.get("SSL_CERT_PATH")
