from db import AutoBotDB as Db
from psycopg2 import sql


class AutoBotTgUsersDB(Db):
    """
    Main Postgres DB functions for tg_users
    """
    db_table_name = 'tg_users'

    def add_tg_user_start(self, _chat_id, _tg_username, _tg_firstname, _tg_lastname):
        try:
            query = sql.SQL("INSERT INTO tg_users(chat_id, tg_username, tg_firstname, tg_lastname) "
                            "VALUES ({chat_id},{tg_username},{tg_firstname},{tg_lastname}) RETURNING chat_id;").format(
                chat_id=sql.Literal(_chat_id),
                tg_username=sql.Literal(_tg_username),
                tg_firstname=sql.Literal(_tg_firstname),
                tg_lastname=sql.Literal(_tg_lastname),
            )
            self.cursor.execute(query)
            self.connect.commit()
            chat_id = self.cursor.fetchone()[0]
            print(f'{chat_id} {_tg_username} {_tg_firstname} {_tg_lastname} added to DB')
            return chat_id
        except Exception as ex:
            print(ex)
            print(f'Error adding user to tg_user relation to DB')

    def add_tg_user_register(self, _tg_users_id, _fk_tg_users_users, _chat_id):
        try:
            query = sql.SQL("UPDATE tg_users SET tg_users_id={tg_users_id}, fk_tg_users_users={fk_tg_users_users} "
                            "WHERE tg_users.chat_id={chat_id};").format(
                tg_users_id=sql.Literal(_tg_users_id),
                fk_tg_users_users=sql.Literal(_fk_tg_users_users),
                chat_id=sql.Literal(_chat_id)
            )
            self.cursor.execute(query)
            self.connect.commit()

        except Exception as ex:
            print(ex)
            print(f'Error adding car to DB')


# add_tg_user = AutoBotTgUsersDB()
# add_tg_user.add_tg_user_register(5685602622, 33, 84891021)