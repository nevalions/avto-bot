import psycopg2
from psycopg2 import sql

from config import host, user, password, db_name
import db_main_queries as queries


class AutoBotUserDB:
    db_table_name = 'users'

    def __init__(self, host_db=host, user_db=user, pass_db=password, db=db_name):
        self.host_db = host_db
        self.user_db = user_db
        self.pass_db = pass_db
        self.db = db

        self.connect = psycopg2.connect(
            host=host_db,
            user=user_db,
            password=pass_db,
            database=db
        )
        self.cursor = self.connect.cursor()

    def query_execute(self, query):
        self.cursor.execute(query)
        self.connect.commit()

    def add_user(self, _username, _email):
        try:
            query = sql.SQL("INSERT INTO users(username, email) SELECT {username}, {email} WHERE NOT EXISTS (SELECT "
                            "id FROM users WHERE email = {email}) RETURNING id").format(username=sql.Literal(_username),
                                                                                        email=sql.Literal(_email))

            self.cursor.execute(query)
            self.connect.commit()
            user_id = self.cursor.fetchone()[0]
            print(f'{_username} with ID: {user_id} added to DB')
            return user_id
        except Exception as ex:
            print(ex)
            print(f'Error adding user to DB, user with email {_email} already exist')

    def update_user_username(self, u_email, new_name):
        try:
            key_name = 'email'
            key = u_email
            value_name = 'username'
            new_value = new_name

            query = queries.update_str_value_in_db_by_key(
                self.db_table_name,
                key_name,
                key,
                value_name,
                new_value
            )
            self.cursor.execute(query)
            self.connect.commit()
            if self.cursor.fetchone():
                print(f'User {new_name} with email: {u_email} updated')
            else:
                raise TypeError(f'User with email {u_email} not exist exist')
        except Exception as ex:
            print(ex)
            print(f'Error updating user in DB')

    def get_all_users_in_db(self):
        self.cursor.execute(queries.get_all_rows_from_db(self.db_table_name))
        all_users = self.cursor.fetchall()
        if all_users:
            return all_users
        else:
            print('No users in DB')
            raise Exception

    def get_user_by_user_id(self, user_id: int):
        query = queries.get_db_item_by_id(self.db_table_name, user_id)
        self.cursor.execute(query)
        car = self.cursor.fetchall()
        if car:
            return car[0]
        else:
            print(f'No users with ID {user_id}')
            raise Exception

    def close(self):
        self.cursor.close()
        self.connect.close()


def main():
    try:
        db = AutoBotUserDB()
        print(db.get_all_users_in_db())
    except Exception as ex:
        print(ex)
    finally:
        db.close()


if __name__ == '__main__':
    main()
