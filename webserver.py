from flask import Flask, jsonify, redirect, render_template, request, json
import database_manager
import constants

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scout_form', methods=['POST', 'GET'])
def scout_form():
    if request.method == 'POST':
        all_cols = constants.all_scouting_data_columns
        values = []
        for col in all_cols:
            value = request.form.get(col)
            values.append(value)

        database_manager.insert_data('scouting_data', all_cols, values)

        return redirect('/basic_results')
    return render_template('scout_form.html')

@app.route('/basic_results', methods=['GET'])
def basic_results():
    columns = constants.all_scouting_data_columns
    data = database_manager.get_recent_data('scouting_data', 'scout_data_id', columns)
    return render_template('RDBMS_Templates/basic_results.html', data=data, search_message='Résultats récents', columns=columns, search_types=constants.basic_search_types)

@app.route('/basic_search', methods=['POST'])
def basic_search():
    search_type = request.form.get('searchType')
    query = request.form.get('query')

    if search_type and query:
        results = database_manager.search_data('scouting_data', search_type, query)
        return render_template('RDBMS_Templates/basic_results.html', data=results, search_message=f'Résultats de la recherche pour "{query.upper()}"', search_types=constants.basic_search_types, columns=constants.all_scouting_data_columns[:3])

    return redirect('/')

@app.route('/advanced_results', methods=['GET', 'POST'])
def advanced_results(table='scouting_data'):
    columns = constants.all_scouting_data_columns
    data = database_manager.get_recent_data(table, 'scout_data_id', columns)
    search_types = constants.advanced_search_types
    return render_template('RDBMS_Templates/advanced_results.html', data=data, search_message='Résultats récents', search_types=search_types, columns=columns)

@app.route('/advanced_search', methods=['POST'])
def advanced_search(table='scouting_data'):
    search_types = constants.advanced_search_types
    if request.method == 'POST':
        search_type = request.form.get('searchType')
        query = request.form.get('query')
        operator = request.form.get('comparator')

        if operator == 'equals':
            results = database_manager.advanced_search(table, search_type, query, '=')
        elif operator == 'not_equals':
            results = database_manager.advanced_search(table, search_type, query, '!=')
        elif operator == 'greater_than':
            results = database_manager.advanced_search(table, search_type, query, '>')
        elif operator == 'less_than':
            results = database_manager.advanced_search(table, search_type, query, '<')

        if search_type and query:
            return render_template('RDBMS_Templates/advanced_results.html', data=results, search_message=f'Résultats pour {search_type} {operator} {query.upper()}', search_types=search_types)

        return redirect('/advanced_results')
    
@app.route('/get_scouting_details/<int:scout_id>')
def get_scouting_details(scout_data_id):
    conn = database_manager.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM scouting_data WHERE scout_data_id = ?", (scout_data_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        columns = [desc[0] for desc in cursor.description]
        data = dict(zip(columns, row))
        return jsonify(data)
    else:
        return jsonify({"error": "Not found"}), 404
