import sqlite3
import constants

DB_NAME = ':memory:' if constants.IN_MEMORY_DB else 'scouting_app.db'

def get_connection():
    conn=sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def insert_data(table, args, data):
    conn = get_connection()
    cursor = conn.cursor()

    if (len(data) != len(args)):
        raise ValueError("Data length does not match arguments length")

    if isinstance(args, list):
        placeholders = ', '.join(['?'] * len(args))
        query = f'INSERT INTO {table} ({", ".join(args)}) VALUES ({placeholders})'
        cursor.execute(query, data)
        print(f'Inserted data into {table}: {data}')

    conn.commit()
    conn.close()

def get_recent_data(table, table_id, columns, limit=10):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    if isinstance(columns, list):
        cursor.execute('SELECT {} FROM {} ORDER BY {} DESC'.format(', '.join(columns), table, table_id))
    elif isinstance(columns, str):
        cursor.execute('SELECT {} FROM {} ORDER BY {} DESC'.format(columns, table, table_id))
    else:
        cursor.execute('SELECT * FROM {} ORDER BY {} DESC'.format(table, table_id))
    rows = cursor.fetchmany(limit)
    conn.close()
    return rows

def search_data(table, search_type, query, limit=10):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM {} WHERE {} LIKE ?'.format(table, search_type), (query))

    rows = cursor.fetchmany(limit)
    conn.close()
    return rows

def advanced_search(table, search_type, query, operator):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = "SELECT * FROM {} WHERE {} {} {}".format(table, search_type, operator, query)
    print(query)
    cursor.execute(query)

    rows = cursor.fetchall()
    conn.close()
    return rows

def create_table(table_name, columns, special_args=None):
    conn = get_connection()
    cursor = conn.cursor()

    column_defs = [f"{name} {dtype}" for name, dtype in columns.items()]
    if special_args:
        column_defs.extend(special_args)

    query = f'CREATE TABLE IF NOT EXISTS {table_name} ({", ".join(column_defs)});'

    cursor.execute(query)
    print(f'Creating table {table_name} with query: {query}')
    conn.commit()
    conn.close()

def get_column_descriptions(table):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table})")
    columns = cursor.fetchall()
    conn.close()
    return columns