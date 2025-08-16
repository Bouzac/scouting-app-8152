import database_manager

def teams_table():
    database_manager.create_table('teams', {
        'team_id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'team_number': 'INTEGER NOT NULL UNIQUE',
        'team_name': 'TEXT',
        'robot_weight': 'REAL',
        'robot_height': 'REAL',
        'robot_width': 'REAL',
        'robot_drive_type': 'TEXT',
        'notes': 'TEXT'
    })

def scouts_table():
    
    database_manager.create_table('scouts', {
        'scout_id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'name': 'TEXT NOT NULL',
        'notes': 'TEXT'
    })

def events_table():
    
    database_manager.create_table('events', {
        'event_id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'name': 'TEXT NOT NULL',
        'start_date': 'TEXT',
        'end_date': 'TEXT',
        'location': 'TEXT',
        'notes': 'TEXT'
    })

def matches_table():
    
    database_manager.create_table('matches', {
        'match_id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'event_id': 'INTEGER',
        'match_number': 'INTEGER NOT NULL',
        'scheduled_time': 'TEXT',
        'score_blue': 'INTEGER DEFAULT 0',
        'score_red': 'INTEGER DEFAULT 0',
        'winning_alliance': 'TEXT',
    }, {
        'UNIQUE(event_id, match_number)',
        'FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE CASCADE'
    })

def scouting_data_table():
    
    database_manager.create_table('scouting_data', {
        'scout_data_id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'match_id': 'INTEGER NOT NULL',
        'team_id': 'INTEGER NOT NULL',
        'scout_id': 'INTEGER NOT NULL',
        'auto_points': 'INTEGER NOT NULL',
        'teleop_points': 'INTEGER NOT NULL',
        'endgame_points': 'INTEGER NOT NULL',
        'penalties': 'INTEGER NOT NULL',
        'robot_status': 'TEXT NOT NULL',
        'notes': 'TEXT',
        'timestamp': 'REAL NOT NULL'
    })

def match_alliances_table():
    database_manager.create_table('match_alliances', {
        'match_alliance_id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'match_id': 'INTEGER NOT NULL',
        'team_id': 'INTEGER NOT NULL',
        'alliance': 'TEXT NOT NULL',
        'score': 'INTEGER NOT NULL'
    })

def init_tables():
    matches_table()