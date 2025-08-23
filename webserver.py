from datetime import datetime
from flask import Flask, jsonify, redirect, render_template, request, Response, url_for, session, flash
import database_manager as db_m
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import constants
import pytesseract
import cv2
from PIL import Image
import os
import re
import tables
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
tables.init_tables()

users = {
    os.getenv("ADMIN_EMAIL"): os.getenv("ADMIN_PASSWORD")
}

@app.route('/')
def index():
    ranking = db_m.get_ranking_data_by_points()
    return render_template('index.html', ranking=ranking)

@app.route('/scout_form', methods=['POST', 'GET'])
def scout_form():
    if request.method == 'POST':
        all_cols = constants.all_scouting_data_columns
        values = [
            request.form.get('scout_data_id'),
            db_m.get_id_by_arg(table='scouts', param='initials', arg=request.form.get('scout_name').lower(), id_type='scout_id'),
            db_m.get_id_by_arg(table='teams', param='team_number', arg=request.form.get('team_number'), id_type='team_id'),
            db_m.get_id_by_arg(table='matches', param='match_number', arg=request.form.get('match_number'), id_type='match_id'),
            request.form.get('auto_points'),
            request.form.get('teleop_points'),
            request.form.get('endgame_points'),
            request.form.get('penalties'),
            request.form.get('robot_status'),
            request.form.get('notes'),
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ]
        db_m.insert_data('scouting_data', all_cols, values)

        return redirect('/basic_results')
    return render_template('scout_form.html')

@app.route('/basic_results', methods=['GET'])
def basic_results():
    columns = constants.all_scouting_data_columns
    columns = parse_columns(columns)
    data = db_m.get_recent_data('scouting_data', 'scout_data_id', columns)
    
    return render_template('RDBMS_Templates/basic_results.html', data=data, search_message='Résultats récents', columns=columns, search_types=constants.basic_search_types)

@app.route('/basic_search', methods=['POST'])
def basic_search():
    search_type = request.form.get('searchType')
    query = request.form.get('query')
    columns = constants.all_scouting_data_columns[:4]
    columns = parse_columns(columns)

    if search_type and query:
        results = db_m.search_data(base_table='scouting_data', search_type=search_type, search_query=query, cols=columns)
        return render_template('RDBMS_Templates/basic_results.html', data=results, search_message=f'Résultats de la recherche pour "{query.upper()}"', search_types=constants.basic_search_types, columns=constants.all_scouting_data_columns[:3])

    return redirect('/')

@app.route('/advanced_results', methods=['GET', 'POST'])
def advanced_results(table='scouting_data'):
    columns = constants.all_scouting_data_columns
    columns = parse_columns(columns)
    data = db_m.get_recent_data(table=table, table_id='scout_data_id', columns=columns)
    search_types = constants.advanced_search_types
    return render_template('RDBMS_Templates/advanced_results.html', data=data, search_message='Résultats récents', search_types=search_types, columns=columns)

@app.route('/advanced_search', methods=['POST'])
def advanced_search(table='scouting_data'):
    search_types = constants.advanced_search_types
    all_columns = constants.all_scouting_data_columns
    columns = parse_columns(all_columns)
    if request.method == 'POST':
        search_type = request.form.get('searchType')
        query = request.form.get('query')
        operator = request.form.get('comparator')

        if operator == 'equals':
            results = db_m.search_data(base_table=table, search_type=search_type, search_query=query, operator='=', cols=columns)
        elif operator == 'not_equals':
            results = db_m.search_data(base_table=table, search_type=search_type, search_query=query, operator='!=', cols=columns)
        elif operator == 'greater_than':
            results = db_m.search_data(base_table=table, search_type=search_type, search_query=query, operator='>', cols=columns)
        elif operator == 'less_than':
            results = db_m.search_data(base_table=table, search_type=search_type, search_query=query, operator='<', cols=columns)

        if search_type and query:
            return render_template('RDBMS_Templates/advanced_results.html',columns=columns ,data=results, search_message=f'Résultats pour {search_type} {operator} {query.upper()}', search_types=search_types)

        return redirect('/advanced_results')
    
@app.route('/get_scouting_details/<int:scout_data_id>')
def get_scouting_details(scout_data_id):
    scouting_data_cols=constants.all_scouting_data_columns
    columns = parse_columns(scouting_data_cols)

    row = db_m.search_data(
        base_table='scouting_data',
        search_type='scout_data_id',
        search_query=scout_data_id,
        cols=columns,
        limit=1
    )

    if row:
        row = row[0]
        data = dict(row)
        return jsonify(data)
    else:
        return jsonify({"error": "Not found"}), 404

def parse_columns(columns):
    display_columns = []
    for col in columns:
        if col == "scout_id":
            display_columns.append("scouts.initials")
        elif col == "team_id":
            display_columns.append("teams.team_number")
        elif col == "match_id":
            display_columns.append("matches.match_number")
        elif col == "notes":
            display_columns.append("scouting_data.notes")
        else:
            display_columns.append(col)
    return display_columns

@app.route('/reports')
def reports():
    return render_template('RDBMS_Templates/reports/reports.html')

@app.route('/reports/<int:team_number>')
def report_details(team_number):
    

    order_by = request.args.get('order_by', default='scout_data_id')
    reverse = request.args.get('reverse', default='0') == '1'

    columns = parse_columns(constants.all_scouting_data_columns)
    columns.pop(0)  # Remove 'scout_data_id' from display columns
    columns.pop(1)  # Remove 'team_number' from display columns

    data = db_m.search_data(
        base_table='scouting_data',
        search_type='teams.team_number',
        search_query=team_number,
        operator="=",
        cols=columns
    )

    event_data = db_m.search_data(
        base_table='scouting_data',
        cols=['auto_points',
              'teleop_points',
              'endgame_points'
        ]
    )

    if not data:
        return f"Aucune donnée trouvée pour l'équipe {team_number}"

    df = pd.DataFrame(data, columns=columns) 
    event_df = pd.DataFrame(event_data, columns=['auto_points', 'teleop_points', 'endgame_points'])

    if order_by in df.columns:
        df.sort_values(by=order_by, ascending=not reverse, inplace=True)

    auto_avg = df['auto_points'].mean()
    teleop_avg = df['teleop_points'].mean()
    endgame_avg = df['endgame_points'].mean()
    event_auto_avg = event_df['auto_points'].mean()
    event_teleop_avg = event_df['teleop_points'].mean()
    event_endgame_avg = event_df['endgame_points'].mean()

    fig, ax = plt.subplots()
    ax.bar(['Auto', 'Teleop', 'Endgame'], [auto_avg, teleop_avg, endgame_avg])
    ax.set_title(f"Performance moyenne de l\'équipe {team_number}")

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    photo_url = base64.b64encode(img.getvalue()).decode()

    return render_template(
        'RDBMS_Templates/reports/team_report.html', 
        team_number=team_number,
        data=df.to_dict(orient='records'),
        photo_url=photo_url,
        auto_avg=auto_avg,
        teleop_avg=teleop_avg,
        endgame_avg=endgame_avg,
        current_sort=order_by,
        reverse=reverse,
        columns=columns,
        auto_event_avg=event_auto_avg,
        teleop_event_avg=event_teleop_avg,
        endgame_event_avg=event_endgame_avg
    )

@app.route('/export_csv/<int:team_number>')
def export_csv(team_number):

    data = db_m.search_data(
        base_table='scouting_data',
        search_type='teams.team_number',
        search_query=team_number,
        cols=parse_columns(constants.all_scouting_data_columns)
    )

    if not data:
        return f"Aucune donnée pour l'équipe {team_number}"

    df = pd.DataFrame(data, columns=parse_columns(constants.all_scouting_data_columns))

    csv_data = df.to_csv(index=False, sep=',', encoding='utf-8-sig')
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment; filename=rapport_team_{team_number}.csv"}
    )

@app.route('/compare_teams')
def compare_teams():
    import pandas as pd
    import matplotlib.pyplot as plt
    import io
    import base64

    team1 = request.args.get('team1', type=int)
    team2 = request.args.get('team2', type=int)
    order_by = request.args.get('order_by', default='scout_data_id')
    reverse = request.args.get('reverse', default='0') == '1'

    if not team1 or not team2:
        return "Deux numéros d'équipe sont requis."

    cols = parse_columns(constants.all_scouting_data_columns)
    cols.pop(0)  # Remove 'scout_data_id' from display columns

    # Récupérer données pour chaque équipe
    data1 = db_m.search_data(
        base_table='scouting_data', 
        search_type='teams.team_number', 
        search_query=team1, 
        cols=cols
    )
    data2 = db_m.search_data(
        base_table='scouting_data', 
        search_type='teams.team_number', 
        search_query=team2, 
        cols=cols
    )

    if not data1 or not data2:
        return "Données manquantes pour une ou les deux équipes."

    df1 = pd.DataFrame(data1, columns=cols)
    df2 = pd.DataFrame(data2, columns=cols)

    # Trier si besoin
    if order_by in df1.columns and order_by in df2.columns:
        df1.sort_values(by=order_by, ascending=not reverse, inplace=True)
        df2.sort_values(by=order_by, ascending=not reverse, inplace=True)

    # Calcul stats clés
    def compute_stats(df):
        return {
            'auto_points': df['auto_points'].mean(),
            'teleop_points': df['teleop_points'].mean(),
            'endgame_points': df['endgame_points'].mean(),
            'penalties': df['penalties'].mean(),
            'matches_played': df['matches.match_number'].nunique(),
            'robot_status_counts': df['robot_status'].value_counts().to_dict()
        }

    stats1 = compute_stats(df1)
    stats2 = compute_stats(df2)

    # Création graphique comparatif
    labels = ['Auto', 'Teleop', 'Endgame', 'Penalties']
    values1 = [stats1['auto_points'], stats1['teleop_points'], stats1['endgame_points'], stats1['penalties']]
    values2 = [stats2['auto_points'], stats2['teleop_points'], stats2['endgame_points'], stats2['penalties']]

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    photo_url = base64.b64encode(img.getvalue()).decode()

    return render_template('RDBMS_Templates/reports/compare_teams.html',
        team1=team1, team2=team2,
        stats1=stats1, stats2=stats2,
        photo_url=photo_url,
        data1=df1.to_dict(orient='records'),
        data2=df2.to_dict(orient='records'),
        columns=cols,
        current_sort=order_by,
        reverse=reverse
    )

@app.route('/compare_teams_form', methods=['GET', 'POST'])
def compare_teams_form():
    if request.method == 'POST':
        team1 = request.form.get('team1', type=int)
        team2 = request.form.get('team2', type=int)
        if not team1 or not team2:
            error = "Veuillez entrer deux numéros d'équipe valides."
            return render_template('compare_teams_form.html', error=error)
        return redirect(url_for('compare_teams', team1=team1, team2=team2))
    return render_template('compare_teams_form.html')

def insert_schedule(schedule_path):
    img = cv2.imread(schedule_path)

    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    custom_config = r'--oem 3 --psm 6'

    text = pytesseract.image_to_string(thresh, config=custom_config, lang='eng')

    lines = text.strip().split('\n')
    lines = [line for line in lines if line.strip()]

    data = []

    for line in lines:
        # Nettoyage des caractères OCR corrompus
        line = re.sub(r'[¢+@_]', '', line)
        line = re.sub(r'\s+', ' ', line).strip()

        # Extraire le nom du match
        match_match = re.search(r'(Qualification \d+)', line)
        match_name = match_match.group(1) if match_match else None

        # Extraire la date/heure (ex: "3/7 - 8:49 AM")
        time_match = re.search(r'\d+/\d+\s*-\s*\d+:\d+\s+[AP]M', line)
        start_time = time_match.group(0) if time_match else None

        # Extraire les numéros d'équipe (6 de suite, 3 chiffres ou plus)
        teams = re.findall(r'\b\d{3,4}\b', line)
        if match_name and start_time and len(teams) >= 6:
            data.append([match_name, start_time] + teams[:6])
        
        match_number = re.sub(r'Qualification (\d+)', r'\1', match_name) if match_name else None


        teams_red = teams[:3]
        teams_blue = teams[3:6]

        db_m.insert_match(
            match_number=match_number,
            teams_red=teams_red,
            teams_blue=teams_blue,
            time=start_time
        )

@app.route('/upload_schedule', methods=['GET', 'POST'])
def upload_schedule():
    if request.method == 'POST':
        schedule_files = request.files.getlist('schedule_files[]')
        if schedule_files:
            for schedule_file in schedule_files:
                schedule_path = f"static/uploads/{schedule_file.filename}"
                schedule_file.save(schedule_path)
                insert_schedule(schedule_path)
            return redirect(url_for('index'))
    return render_template('upload_schedule.html')

@app.route('/page_admin')
def page_admin():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if email in users and users[email] == password:
            session['user'] = email
            return redirect(url_for('dashboard'))
        else:
            flash("Identifiants incorrects")

    return render_template('login.html')
