import psycopg2
from config import host, user, password, db_name


def main():
    test_db()


def test_db():
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT version();'
            )

            print(f'Version {cursor.fetchone()}')

        # with connection.cursor() as cursor:
        #     cursor.execute(
        #         """CREATE TABLE users(
        #         id serial PRIMARY KEY,
        #         name varchar(50) NOT NULL)"""
        #     )

        # with connection.cursor() as cursor:
        #     cursor.execute(
        #         """INSERT INTO users (name) VALUES
        #         ('test user')"""
        #     )

        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT * FROM public.users"""
            )

            print(f'Version {cursor.fetchall()}')
        #
        #     with connection.cursor() as cursor:
        #         cursor.execute(
        #             """DELETE FROM users WHERE id = 3"""
        #         )

    except Exception as ex:
        print(ex)

    finally:
        if connection:
            connection.close()
            print('[INFO] Postgres connection closed')


if __name__ == '__main__':
    main()
