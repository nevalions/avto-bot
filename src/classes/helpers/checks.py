from email_validator import validate_email, EmailNotValidError

import logging.config
from src.logs.log_conf_main import LOGGING_CONFIG
from src.logs.func_auto_log import autolog_info, autolog_warning, autolog_debug

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


def email_is_valid(mail: str):
    autolog_debug(f'Check email {mail}')
    m = mail.strip()
    if m != validate_email(m).email:
        raise EmailNotValidError()

