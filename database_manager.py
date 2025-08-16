import sqlite3
import constants
import tables

DB_NAME = ':memory:' if constants.IN_MEMORY_DB else 'scouting_app.db'

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    update_db()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scout_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scoutID TEXT NOT NULL,
            teamNumber INTEGER NOT NULL,
            matchNumber INTEGER NOT NULL
        );
    ''')
    conn.commit()
    conn.close()

def update_db():
    conn = get_connection()
    cursor = conn.cursor()

    search_types = constants.advanced_search_types()

    cursor.execute("SELECT name FROM PRAGMA_TABLE_INFO('scout_data');")
    columns = cursor.fetchall()
    columns.remove(('id',),)
    
    for search_type in search_types:
        if (search_type['value'],) not in columns:
            cursor.execute(f'ALTER TABLE scout_data ADD COLUMN {search_type["value"]} {search_type["type"].upper()}')
            print(f'Added column {search_type["value"]} to scout_data as {search_type["type"].upper()}')

    for c in columns:
        if c[0] not in [s['value'] for s in search_types]:
            cursor.execute(f'ALTER TABLE scout_data DROP COLUMN {c[0]}')
            print(f'Dropped column {c[0]} from scout_data')

    conn.commit()
    conn.close()

def insert_scout_data(scoutID, teamNumber, matchNumber):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO scout_data (scoutID, teamNumber, matchNumber)
        VALUES (?, ?, ?)
    ''', (scoutID, teamNumber, matchNumber))
    conn.commit()
    conn.close()

def get_recent_data():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM scout_data ORDER BY id DESC')
    rows = cursor.fetchmany(10)
    conn.close()
    return rows

def search_data(search_type, query):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM scout_data WHERE {} LIKE ?'.format(search_type), ('%' + query + '%',))

    rows = cursor.fetchall()
    conn.close()
    return rows

def advanced_search(search_type, query, operator):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = "SELECT * FROM scout_data WHERE {} {} {}".format(search_type, operator, query)
    print(query)
    cursor.execute(query)

    rows = cursor.fetchall()
    conn.close()
    return rows

def create_table(table_name, columns, special_args):
    conn = get_connection()
    cursor = conn.cursor()

    columns_with_types = ', '.join(['{} {}'.format(name, dtype) for name, dtype in columns.items()])
    query = 'CREATE TABLE IF NOT EXISTS {} ({})'.format(table_name, columns_with_types)

    if special_args:
        query += ', {}'.format(', '.join(special_args))

    cursor.execute(query)

    conn.commit()
    conn.close()