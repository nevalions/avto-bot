from psycopg2 import sql


def get_db_item_by_id(_table, _id):
    return sql.SQL("SELECT * FROM {table} WHERE {table}.id={item_id}").format(
        table=sql.Identifier(_table),
        item_id=sql.Literal(_id)
    )


def get_all_rows_from_db(_table):
    return sql.SQL("SELECT * FROM {table}").format(table=sql.Identifier(_table))


