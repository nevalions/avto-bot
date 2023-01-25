from psycopg2 import sql

import db_queries as queries
from db import AutoBotDB as Db


class AutoBotMainDB(Db):
    def add_car_to_user_in_db(self, _user_id, _car_id):
        try:
            query = queries.create_m2m_relation(_user_id, _car_id)
            self.cursor.execute(query)
            self.connect.commit()
            print(f'Car ID({_car_id}) added to user ID({_user_id})')
            return _user_id, _car_id
        except Exception as ex:
            print(ex)
            print(f'Error adding car to user')
