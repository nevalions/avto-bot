import string

import checks


class User:
    # user class
    def __init__(self, username: str, email: str):
        # self.not_empty_str(name)
        # self.check_email(email)

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
        if type(txt) != str:
            raise TypeError('User name must be str type')
        if len(txt.strip()) < 3:
            raise TypeError('User name must be minimum 3 letters')

    @classmethod
    # check is object fields not empty to print
    def __is_valid_to_print(cls, name, mail):
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
        try:
            self.not_empty_str(username)
            self._username = username.strip().translate(str.maketrans('', '', string.punctuation))
        except Exception as ex:
            print(str(ex))
            print('User not updated')
            raise ex

    @property
    # user email
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        try:
            self.check_email(email)
            self._email = email.strip()
        except Exception as ex:
            print(str(ex))
            print('User not updated')
            raise ex

    def print_user_info(self):
        # print user info (name, email)
        try:
            self.__is_valid_to_print(self._username, self._email)
            print(f'Name: {self._username}, email: {self._email}')
        except Exception as ex:
            print(str(ex))
            print('Not able to print user')


def main():
    user = User('asd', 'asd@asd.ru')
    print(user)

    try:
        user2 = User('', 'asd@asd1.ru')
        print(user2)
    except Exception as ex:
        print(ex)

    try:
        user3 = User('asfasgv', 'asdasd')
        print(user3)
    except Exception as ex:
        print(ex)

    user_diction = vars(user)
    print(user_diction)

    print({(k[1:]): v for k, v in user_diction.items()})


if __name__ == '__main__':
    main()
