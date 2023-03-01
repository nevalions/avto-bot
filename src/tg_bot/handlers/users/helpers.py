import logging.config

from aiogram.types import Message

from src.logs.log_conf_main import LOGGING_CONFIG

from src.tg_bot.keybords.inline import ikb_menu

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)
