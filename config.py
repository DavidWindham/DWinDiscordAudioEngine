import os

# from os.path import join, dirname
from dotenv import load_dotenv

# load_dotenv(join(dirname(__file__), '.env'))
load_dotenv()

DISCORD_TOKEN = os.environ.get("TOKEN")
DB_URI = os.environ.get('DB_URI')
DB_PORT = os.environ.get('DB_PORT')
