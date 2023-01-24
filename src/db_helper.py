import psycopg2
from psycopg2 import sql

from config import host, user, password, db_name


class AutoBotDB:
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

    def add_user(self, query):
        pass

    def add_car(self, model, model_name, mileage, measures, date_added, description):
        query = "INSERT INTO cars(model, model_name, mileage, measures, date_added, description) "\
                  "VALUES(%s,%s,%s,%s,%s,%s) RETURNING id;"
        self.cursor.execute(query, (model, model_name, int(mileage), measures, date_added, description))
        self.connect.commit()

        print(self.cursor.fetchone()[0])

    def close(self):
        self.cursor.close()
        self.connect.close()


def main():
    try:
        db = AutoBotDB()
        db.add_car('Gmc', 'Savana', '300000', 'miles', '22.01.2023', 'BLABLABLA')
    except Exception as ex:
        print(ex)
    finally:
        db.close()


if __name__ == '__main__':
    main()
