from flask import (Flask, render_template, request, redirect, url_for, flash,
jsonify)
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

CATEGORIES = [{'id':'1', 'name':'Fat Loss'}, {'id':'2', 'name':'Muscle Gain'},
    {'id':'3', 'name':'Strength Gain'}, {'id':'4', 'name':'Well Being'}]

EXERCISES = [{'id': '1', 'name':'Kettlebell Swings', 'category_id':'2',
    'url':'https://www.youtube.com/watch?v=-KqxcDijOyA', 'description':"""
    A simple tool to add strength and build the posterior chain."""},
    {'id': '2', 'name':'Running', 'category_id':'1',
    'url':'https://www.youtube.com/watch?v=8XiwtiDTlYU', 'description':"""
    Classic exercise that few know with proper technique."""}]

@app.route('/')
@app.route('/index.html')
@app.route('/index.html/')
def index():
    return render_template("index.html", categories=CATEGORIES,
        exercises=EXERCISES)

@app.route('/login')
@app.route('/login/')
def login():
    return render_template("login.html")

@app.route('/<goal>')
@app.route('/<goal>/')
def view_goal(goal):
    return render_template("view-goal.html")

@app.route('/<goal>/<exercise>')
@app.route('/<goal>/<exercise>/')
def view_exercise(goal, exercise):
    return render_template("view-exercise.html")

@app.route('/how-it-works')
@app.route('/how-it-works/')
def how_it_works():
    return render_template("how-it-works.html")

@app.route('/<goal>/new')
@app.route('/<goal>/new/')
def new_exercise(goal):
    return render_template("new-exercise.html")

@app.route('/<goal>/<exercise>/edit')
@app.route('/<goal>/<exercise>/edit/')
def edit_exercise(goal, exercise):
    return render_template("edit-exercise.html")

@app.route('/<goal>/<exercise>/delete')
@app.route('/<goal>/<exercise>/delete/')
def delete_exercise(goal, exercise):
    return render_template("delete-exercise.html")

def get_category(category_id):
    return CATEGORIES[0]['name']

app.jinja_env.globals.update(get_category=get_category)

if __name__ == "__main__":
    app.secret_key = "supersupersecretkey"
    app.debug = True
    app.run(host = '0.0.0.0', port=8000)
