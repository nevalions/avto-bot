import logging.config
import string

from log_dir.log_conf import LOGGING_CONFIG
from log_dir.func_auto_log import autolog_debug, autolog_info
import checks

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


class User:
    # user class
    def __init__(self, username: str, email: str):
        autolog_debug(f'User class called')
        self.username = username.strip()
        self.email = email.strip()

    def __str__(self):
        return f'{self.username}, {self.email}'

    def __getattr__(self, attr):
        return self[attr]

    @classmethod
    # check is email valid
    def check_email(cls, mail):
        checks.email_is_valid(mail)

    @classmethod
    # check string is valid
    def not_empty_str(cls, txt):
        autolog_debug(f'User class check "{txt}"')
        if type(txt) != str:
            raise TypeError('User name must be str type')
        if len(txt.strip()) < 3:
            raise TypeError('User name must be minimum 3 letters')

    @classmethod
    # check is object fields not empty to print
    def __is_valid_to_print(cls, name, mail):
        autolog_debug(f'User class check is valid for print')
        if not name:
            raise TypeError('User name empty')
        if not mail:
            raise TypeError('User email empty')

    @property
    # username
    def username(self):
        return self._username

    @username.setter
    def username(self, username):
        autolog_debug(f'User username enter "{username}"')
        try:
            self.not_empty_str(username)
            self._username = username.strip().translate(str.maketrans('', '', string.punctuation))
        except Exception as ex:
            logging.error(ex)
            raise ex

    @property
    # user email
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        autolog_debug(f'User email enter "{email}"')
        try:
            self.check_email(email)
            self._email = email.strip()
        except Exception as ex:
            logging.error(ex)
            raise ex

    def print_user_info(self):
        # print user info (name, email)
        try:
            self.__is_valid_to_print(self._username, self._email)
            print(f'Name: {self._username}, email: {self._email}')
        except Exception as ex:
            logging.error(ex)


def main():
    user = User('asd', 'asd@asd.ru')

    print(user)

    try:
        user2 = User('', 'asd@asd1.ru')
        print(user2)
    except Exception as ex:
        autolog_info('Not valid user')
        print(ex)

    try:
        user3 = User('asfasgv', 'asdasd')
        print(user3)
    except Exception as ex:
        autolog_info('Not valid user')
        print(ex)
    #
    # user_diction = vars(user)
    # print(user_diction)
    #
    # print({(k[1:]): v for k, v in user_diction.items()})


if __name__ == '__main__':
    main()
