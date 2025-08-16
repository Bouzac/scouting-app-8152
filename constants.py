def basic_search_types():
    s = [{"value": "scoutID", "label": "Scout ID"},
         {"value": "teamNumber", "label": "Team Number"},
         {"value": "matchNumber", "label": "Match Number"}]
    return s

def advanced_search_types():
    s = [{"value": "scoutID", "label": "Scout ID", "type": "text"},
         {"value": "teamNumber", "label": "Team Number", "type": "number"},
         {"value": "matchNumber", "label": "Match Number", "type": "number"},
         ]
    return s

IN_MEMORY_DB = True #For debugging only