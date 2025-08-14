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

@app.route('/results')
def results():
    return render_template('results.html')

@app.route('/scout_form', methods=['POST', 'GET'])
def scout_form():
    if request.method == 'POST':
        scoutID = request.form.get('scoutID')
        teamNumber = request.form.get('team_number')
        matchNumber = request.form.get('match_number')

        database_manager.insert_scout_data(scoutID, teamNumber, matchNumber)

        return redirect('/results')
    return render_template('scout_form.html')