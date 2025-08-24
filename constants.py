basic_search_types = [
    {"value": "scouts.initials", "label": "Initiales de l'éclaireur"},
    {"value": "teams.team_number", "label": "Numéro d'équipe"},
    {"value": "matches.match_number", "label": "Numéro de match"}
]

advanced_search_types = [
    {"value": "scouts.initials", "label": "Initiales de l'éclaireur", "type": "text"},
    {"value": "teams.team_number", "label": "Numéro d'équipe", "type": "number"},
    {"value": "matches.match_number", "label": "Numéro de match", "type": "number"},
    {"value": "auto_points", "label": "Auto Points", "type": "number"},
    {"value": "teleop_points", "label": "Teleop Points", "type": "number"},
    {"value": "endgame_points", "label": "Endgame Points", "type": "number"},
    {"value": "penalties", "label": "Penalties", "type": "number"},
    {"value": "robot_status", "label": "Robot Status", "type": "text"},
    {"value": "scouting_data.notes", "label": "Notes", "type": "text"},
    {"value": "timestamp", "label": "Timestamp", "type": "text"}
]

all_scouting_data_columns = ['scout_data_id','scout_id', 'team_id', 'match_id', 'auto_points', 'teleop_points', 'endgame_points', 'penalties', 'robot_status', 'notes', 'timestamp']
all_scouts_columns = ['scout_id', 'name', 'notes']
all_events_columns = ['event_id', 'name', 'start_date', 'end_date', 'location', 'notes']
all_matches_columns = ['match_id', 'event_id', 'match_number', 'scheduled_time']
all_match_alliances_columns = ['match_alliance_id', 'match_id', 'alliance_color', 'team_id']
all_teams_columns = ['team_id', 'team_number', 'team_name', 'robot_drive_type', 'notes']

STREAM_ON = True
STREAM_URL = 'https://www.twitch.tv/bourzac'
STREAM_COORDS = {
    'match_number': {'top_left': (454, 6), 'bottom_right': (846, 42)},
    'blue_points': {'top_left': (463, 107), 'bottom_right': (581, 188)},
    'red_points': {'top_left': (705, 113), 'bottom_right': (819, 189)},
    'blue_teams': {'top_left': (69, 297), 'bottom_right': (140, 444)},
    'red_teams': {'top_left': (946, 298), 'bottom_right': (1023, 444)},
}

DATABASE_PATH = 'scouting_app.db'
IN_MEMORY_DB = False #For debugging only

MATCH_URLS_2025 = ['https://www.youtube.com/watch?v=6NgmXvXbiAE', 'https://www.youtube.com/watch?v=21mEnSvQhDA', 'https://www.youtube.com/watch?v=37TuyrX8lXY', 'https://www.youtube.com/watch?v=44aftfCHWyA', 'https://www.youtube.com/watch?v=xOij2R77qZk', 'https://www.youtube.com/watch?v=NYD6IZBHjqE', 'https://www.youtube.com/watch?v=axFeaSi63E4', 'https://www.youtube.com/watch?v=edA3G-a0Ku8', 'https://www.youtube.com/watch?v=vBf4OYlp3qk', 'https://www.youtube.com/watch?v=nbClNNBTQek', 'https://www.youtube.com/watch?v=eKdPPndotDs', 'https://www.youtube.com/watch?v=AU3docuC-T8', 'https://www.youtube.com/watch?v=f3kGkvjXDu4', 'https://www.youtube.com/watch?v=gbT_T1FC7XQ', 'https://www.youtube.com/watch?v=I_tbE2X8DBw', 'https://www.youtube.com/watch?v=B8Rlx-TByqc', 'https://www.youtube.com/watch?v=vz0GnSUiHoo', 'https://www.youtube.com/watch?v=2xGoykP71v8', 'https://www.youtube.com/watch?v=uVpsaZo3tnI', 'https://www.youtube.com/watch?v=lDArVFXt5wA', 'https://www.youtube.com/watch?v=9kb4vP_bxWo', 'https://www.youtube.com/watch?v=0VAAW-Tey9s', 'https://www.youtube.com/watch?v=GlEFovwjkDM', 'https://www.youtube.com/watch?v=DR8cFs9sGBw', 'https://www.youtube.com/watch?v=ndtyuqYEbUs', 'https://www.youtube.com/watch?v=3WXQwEYZzvQ', 'https://www.youtube.com/watch?v=B9zP0H9qRvk', 'https://www.youtube.com/watch?v=MWb6VVtKMzg', 'https://www.youtube.com/watch?v=AjzjF8h1Wvk', 'https://www.youtube.com/watch?v=c7pbosLjgd8', 'https://www.youtube.com/watch?v=15TPet3Lsz4', 'https://www.youtube.com/watch?v=LuHPHM6txmo', 'https://www.youtube.com/watch?v=yVzMxHApWZE', 'https://www.youtube.com/watch?v=HT5PcLhdGhQ', 'https://www.youtube.com/watch?v=oHVZtK0nAxM', 'https://www.youtube.com/watch?v=cN4mYlN0Yh8', 'https://www.youtube.com/watch?v=zOeDjdd75jw', 'https://www.youtube.com/watch?v=3CF3di0fZUw', 'https://www.youtube.com/watch?v=2IreQCcM7FI', 'https://www.youtube.com/watch?v=WIFd-cYSsYU', 'https://www.youtube.com/watch?v=dHm-1fpW500', 'https://www.youtube.com/watch?v=updeJxnmnfA', 'https://www.youtube.com/watch?v=WdliZsAKlws', 'https://www.youtube.com/watch?v=EtPclLlcmkc', 'https://www.youtube.com/watch?v=vU1HBEwj888', 'https://www.youtube.com/watch?v=qL01fGY_GFA', 'https://www.youtube.com/watch?v=hLtzx1ToYXk', 'https://www.youtube.com/watch?v=AYwWNMVYJyE', 'https://www.youtube.com/watch?v=oFRfoKlkEcc', 'https://www.youtube.com/watch?v=9XHRE2gNZ8Y', 'https://www.youtube.com/watch?v=FTj2Z66qu0Y', 'https://www.youtube.com/watch?v=8k6ZJ5w880Y', 'https://www.youtube.com/watch?v=KKABB2T2zDE', 'https://www.youtube.com/watch?v=YGCPXxWl3Dw', 'https://www.youtube.com/watch?v=8xYzIUpfrcM', 'https://www.youtube.com/watch?v=PlObV_EyrDo', 'https://www.youtube.com/watch?v=A9vrCFDMHuk', 'https://www.youtube.com/watch?v=WwNVnC59BnM', 'https://www.youtube.com/watch?v=BXqM74Tdi7Y', 'https://www.youtube.com/watch?v=03UybLSWgsY', 'https://www.youtube.com/watch?v=XSuReLBDuuE', 'https://www.youtube.com/watch?v=9LhC_3lmaOQ', 'https://www.youtube.com/watch?v=7u3giUuvfjQ', 'https://www.youtube.com/watch?v=QTSYT7WMyys', 'https://www.youtube.com/watch?v=indlL1o9O0o', 'https://www.youtube.com/watch?v=XCoSfWaMlfM', 'https://www.youtube.com/watch?v=0RVDTOm4aW8', 'https://www.youtube.com/watch?v=4DtWz-6V6Sc', 'https://www.youtube.com/watch?v=w43CfmvFUIw', 'https://www.youtube.com/watch?v=9XniGGh2AQM', 'https://www.youtube.com/watch?v=oWlJK8jFoec', 'https://www.youtube.com/watch?v=u6ZaN_Ns9EM', 'https://www.youtube.com/watch?v=PYpL_4Kncg8', 'https://www.youtube.com/watch?v=X7yhXeAwQLg', 'https://www.youtube.com/watch?v=yw4GS2SdNes', 'https://www.youtube.com/watch?v=n66IdqPnysI', 'https://www.youtube.com/watch?v=zlHV-d1FNtQ', 'https://www.youtube.com/watch?v=DKdrk-2kaCo', 'https://www.youtube.com/watch?v=2InajDCdg_w', 'https://www.youtube.com/watch?v=9_fs__X5FeA', 'https://www.youtube.com/watch?v=2j4vguZ5d6s', 'https://www.youtube.com/watch?v=pOuq5RtDWVU', 'https://www.youtube.com/watch?v=naSyOxPTvXU', 'https://www.youtube.com/watch?v=JLRHbTPKY6I', 'https://www.youtube.com/watch?v=3cRNmCNotzY', 'https://www.youtube.com/watch?v=LNRlG08pYoc', 'https://www.youtube.com/watch?v=9dPbD25PthM', 'https://www.youtube.com/watch?v=m-PGJDn7OC4']