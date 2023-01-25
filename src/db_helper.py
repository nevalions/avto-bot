import psycopg2

from config import host, user, password, db_name


class AutoBotDB:
    cars_db_table_name = 'cars'

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

    def close(self):
        self.cursor.close()
        self.connect.close()


def main():
    try:
        db = AutoBotDB()
        # print(db.get_car_by_car_id(11))
    except Exception as ex:
        print(ex)
    finally:
        db.close()


if __name__ == '__main__':
    main()
