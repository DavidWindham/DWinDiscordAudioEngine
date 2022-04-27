import os
# from os.path import join, dirname
from dotenv import load_dotenv

#load_dotenv(join(dirname(__file__), '.env'))
load_dotenv()

DISCORD_TOKEN = os.environ.get("TOKEN")