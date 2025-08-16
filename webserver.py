from flask import Flask, redirect, render_template, request, json
import database_manager
import constants

app = Flask(__name__)
database_manager.init_db()
database_manager.update_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hello')
def hello():
    return render_template('hello.html')


@app.route('/scout_form', methods=['POST', 'GET'])
def scout_form():
    if request.method == 'POST':
        scoutID = request.form.get('scoutID')
        teamNumber = request.form.get('team_number')
        matchNumber = request.form.get('match_number')

        database_manager.insert_scout_data(scoutID, teamNumber, matchNumber)

        return redirect('/basic_results')
    return render_template('scout_form.html')

@app.route('/basic_results', methods=['GET'])
def basic_results():
    data = database_manager.get_recent_data()
    return render_template('basic_results.html', data=data, search_message='Résultats récents')

@app.route('/basic_search', methods=['POST'])
def basic_search():
    search_type = request.form.get('searchType')
    query = request.form.get('query')

    if search_type and query:
        results = database_manager.search_data(search_type, query)
        return render_template('basic_results.html', data=results, search_message=f'Résultats de la recherche pour "{query.upper()}"')

    return redirect('/')

@app.route('/advanced_results', methods=['GET', 'POST'])
def advanced_results():
    data = database_manager.get_recent_data()
    search_types = constants.advanced_search_types()
    return render_template('advanced_results.html', data=data, search_message='Résultats récents', search_types=search_types)

@app.route('/advanced_search', methods=['POST'])
def advanced_search():
    search_types = constants.advanced_search_types()
    if request.method == 'POST':
        search_type = request.form.get('searchType')
        query = request.form.get('query')
        operator = request.form.get('comparator')

        if operator == 'equals':
            results = database_manager.advanced_search(search_type, query, '=')
        elif operator == 'not_equals':
            results = database_manager.advanced_search(search_type, query, '!=')
        elif operator == 'greater_than':
            results = database_manager.advanced_search(search_type, query, '>')
        elif operator == 'less_than':
            results = database_manager.advanced_search(search_type, query, '<')

        if search_type and query:
            return render_template('advanced_results.html', data=results, search_message=f'Résultats de la recherche avancée pour "{query.upper()}"', search_types=search_types)

        return redirect('/advanced_results')

@app.route('/test')
def test():
    return render_template('test.html')
