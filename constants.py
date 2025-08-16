basic_search_types = [
    {"value": "scout_id", "label": "Scout ID"},
    {"value": "team_id", "label": "Team Number"},
    {"value": "match_id", "label": "Match Number"}
]

advanced_search_types = [
    {"value": "scout_id", "label": "Scout ID", "type": "text"},
    {"value": "team_id", "label": "Team Number", "type": "number"},
    {"value": "match_id", "label": "Match Number", "type": "number"},
    {"value": "auto_points", "label": "Auto Points", "type": "number"},
    {"value": "teleop_points", "label": "Teleop Points", "type": "number"},
    {"value": "endgame_points", "label": "Endgame Points", "type": "number"},
    {"value": "penalties", "label": "Penalties", "type": "number"},
    {"value": "robot_status", "label": "Robot Status", "type": "text"},
    {"value": "notes", "label": "Notes", "type": "text"},
    {"value": "timestamp", "label": "Timestamp", "type": "text"}
]

all_scouting_data_columns = ['scout_data_id','scout_id', 'team_id', 'match_id', 'auto_points', 'teleop_points', 'endgame_points', 'penalties', 'robot_status', 'notes', 'timestamp']
all_scouts_columns = ['scout_id', 'name', 'notes']
all_events_columns = ['event_id', 'name', 'start_date', 'end_date', 'location', 'notes']
all_matches_columns = ['match_id', 'event_id', 'match_number', 'scheduled_time']
all_match_alliances_columns = ['match_alliance_id', 'match_id', 'alliance_color', 'team_id']
all_teams_columns = ['team_id', 'team_number', 'team_name', 'robot_drive_type', 'notes']

DATABASE_PATH = 'scouting_app.db'
IN_MEMORY_DB = False #For debugging only