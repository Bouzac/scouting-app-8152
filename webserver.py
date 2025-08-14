from flask import Flask, redirect, render_template, request
import database_manager

app = Flask(__name__)
database_manager.init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hello')
def hello():
    return render_template('hello.html')

@app.route('/results', methods=['GET'])
def results():
    data = database_manager.get_all_data()
    return render_template('results.html', data=data)

@app.route('/scout_form', methods=['POST', 'GET'])
def scout_form():
    if request.method == 'POST':
        scoutID = request.form.get('scoutID')
        teamNumber = request.form.get('team_number')
        matchNumber = request.form.get('match_number')

        database_manager.insert_scout_data(scoutID, teamNumber, matchNumber)

        return redirect('/results')
    return render_template('scout_form.html')

@app.route('/search', methods=['POST'])
def search():
    search_type = request.form.get('searchType')
    query = request.form.get('query')

    if search_type and query:
        results = database_manager.search_data(search_type, query)
        return render_template('results.html', data=results)

    return redirect('/')
