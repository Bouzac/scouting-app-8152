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
        'initials': 'TEXT NOT NULL',
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
        'match_id': 'INTEGER',
        'team_id': 'INTEGER',
        'scout_id': 'INTEGER',
        'auto_points': 'INTEGER DEFAULT 0',
        'teleop_points': 'INTEGER DEFAULT 0',
        'endgame_points': 'INTEGER DEFAULT 0',
        'penalties': 'INTEGER DEFAULT 0',
        'robot_status': 'TEXT CHECK (robot_status IN (\'working\', \'damaged\', \'disabled\'))',
        'notes': 'TEXT',
        'timestamp': 'TEXT DEFAULT (datetime(\'now\'))'
    }, {
        'UNIQUE(match_id, team_id, scout_id)',
        'FOREIGN KEY (match_id) REFERENCES matches(match_id) ON DELETE CASCADE',
        'FOREIGN KEY (team_id) REFERENCES teams(team_id) ON DELETE CASCADE',
        'FOREIGN KEY (scout_id) REFERENCES scouts(scout_id) ON DELETE CASCADE'
    })

def match_alliances_table():
    database_manager.create_table('match_alliances', {
        'match_alliance_id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'match_id': 'INTEGER',
        'alliance_color': 'TEXT CHECK(alliance_color IN (\'red\', \'blue\'))',
        'team_1_id': 'INTEGER',
        'team_2_id': 'INTEGER',
        'team_3_id': 'INTEGER'
    }, {
        'UNIQUE(match_id, alliance_color)',
        'FOREIGN KEY (match_id) REFERENCES matches(match_id) ON DELETE CASCADE',
        'FOREIGN KEY (team_1_id) REFERENCES teams(team_id)',
        'FOREIGN KEY (team_2_id) REFERENCES teams(team_id)',
        'FOREIGN KEY (team_3_id) REFERENCES teams(team_id)'
    })

def init_tables():
    teams_table()
    scouts_table()
    events_table()
    matches_table()
    scouting_data_table()
    match_alliances_table()