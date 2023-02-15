import sys
import os

from email_validator import validate_email, EmailNotValidError
import logging.config

sys.path.append(os.path.join(os.getcwd(), '..'))
sys.path.append(os.path.join(os.getcwd(), '..'))
from src.log_dir.log_conf import LOGGING_CONFIG
from src.log_dir.func_auto_log import autolog_debug

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


def email_is_valid(mail: str):
    autolog_debug(f'Check email {mail}')
    m = mail.strip()
    if m != validate_email(m).email:
        raise EmailNotValidError()

