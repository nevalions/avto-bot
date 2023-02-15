import os

from dotenv import load_dotenv

load_dotenv()

tg_token = str(os.getenv("BOT_TOKEN"))
admins_id = str(os.getenv('BOT_ADMINS'))
