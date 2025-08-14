import sqlite3

DB_NAME = 'scouting_app.db'

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
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

def insert_scout_data(scoutID, teamNumber, matchNumber):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO scout_data (scoutID, teamNumber, matchNumber)
        VALUES (?, ?, ?)
    ''', (scoutID, teamNumber, matchNumber))
    conn.commit()
    conn.close()

def get_all_data():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM scout_data')
    rows = cursor.fetchall()
    conn.close()
    return rows