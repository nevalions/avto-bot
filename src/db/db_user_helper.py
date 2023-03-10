from psycopg2 import sql

from src.db.db_main import AutoBotDB as Db
from src.db.db_queries import get_all_rows_from_db, update_str_value_in_db_by_key, get_db_item_by_id
from src.db.db_queries import get_db_item_by_name


class AutoBotUserDB(Db):
    """
    Main Postgres DB functions for User()
    """
    db_table_name = 'user'

    def query_execute(self, query):
        self.cursor.execute(query)
        self.connect.commit()

    def add_user(self, _username, _email):
        try:
            query = sql.SQL("INSERT INTO user(username, email) SELECT {username}, {email} WHERE NOT EXISTS (SELECT "
                            "id FROM user WHERE email = {email}) RETURNING id").format(username=sql.Literal(_username),
                                                                                       email=sql.Literal(_email))
            self.cursor.execute(query)
            self.connect.commit()
            try:
                user_id = self.cursor.fetchone()[0]
                if user_id:
                    print(f'User {_username} with ID({user_id}) added to DB')
                    return user_id
            except Exception as ex:
                print(ex)
                print(f'User with email {_email} already exist')
                print(f'Error adding user to DB')

        except Exception as ex:
            print(ex)
            print(f'Error adding user to DB')

    def update_user_username(self, u_email, new_name):
        try:
            key_name = 'email'
            key = u_email
            value_name = 'username'
            new_value = new_name

            query = update_str_value_in_db_by_key(
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
                raise TypeError(f'No User with email {u_email}')
        except Exception as ex:
            print(ex)
            print(f'Error updating user in DB')

    def get_all_users_in_db(self):
        self.cursor.execute(get_all_rows_from_db(self.db_table_name))
        all_users = self.cursor.fetchall()
        if all_users:
            return all_users
        else:
            print('No users in DB')
            raise Exception

    def get_user_by_user_id(self, user_id: int):
        query = get_db_item_by_id(self.db_table_name, user_id)
        self.cursor.execute(query)
        car = self.cursor.fetchall()
        if car:
            return car[0]
        else:
            print(f'No users with ID({user_id})')
            raise Exception

    def search_user_email_in_db(self, item_name, item):
        try:
            query = get_db_item_by_name(self.db_table_name, item_name, item)
            result = self.select_query_dict(query)
            if result:
                return result
            else:
                print(f'No email in DB')
                return None
        except Exception as ex:
            print(ex)


def main():
    db = AutoBotUserDB()
    try:
        print(db.get_all_users_in_db())
    except Exception as ex:
        print(ex)
    finally:
        db.close()


if __name__ == '__main__':
    main()
