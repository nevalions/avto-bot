import pytest

from src.classes.users import User

user1 = User('Test', 'asd@asd.ru')


def main():
    test_users_ok()
    test_update_fields()
    test_strip_ok()
    test_user_exceptions()


def test_users_ok():
    assert user1.username == 'Test'
    assert user1.email == 'asd@asd.ru'


def test_update_fields():
    user1.username = 'Super Jhon'
    user1.email = 'asd@asd1.ru'

    assert user1.username == 'Super Jhon'
    assert user1.email == 'asd@asd1.ru'


def test_strip_ok():
    user1.username = '              Super Jhon         '
    user1.email = '        asd@asd1.ru        '

    assert user1.email == 'asd@asd1.ru'
    assert user1.username == 'Super Jhon'


def test_user_exceptions():
    with pytest.raises(Exception):
        user1.username = 'G'
    with pytest.raises(Exception):
        user1.username = 'Ga'
    with pytest.raises(Exception):
        user1.email = 'asd@asd.ruasfas'

    with pytest.raises(Exception):
        User('       ', 'asd@asd.ru')
    with pytest.raises(Exception):
        User('asdasf', '           ')
    with pytest.raises(Exception):
        User('as', 'asd@asd.ru')
    with pytest.raises(Exception):
        User(123, 'asd@asd.ru')
    with pytest.raises(Exception):
        User('asd', 123)


if __name__ == '__main__':
    main()
