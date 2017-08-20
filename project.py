from flask import (Flask, render_template, request, redirect, url_for, flash,
jsonify)
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@app.route('/')
@app.route('/index.html')
def index():
    return render_template("index.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/<goal>')
def view_goal(goal):
    return render_template("view-goal.html")

@app.route('/<goal>/<workout>')
def view_workout(goal, workout):
    return render_template("view-workout.html")

@app.route('/how-it-works')
def how_it_works():
    return render_template("how-it-works.html")

@app.route('/<goal>/new')
def new_workout(goal):
    return render_template("new-workout.html")

@app.route('/<goal>/<workout>/edit')
def edit_workout(goal, workout):
    return render_template("edit-workout.html")

@app.route('/<goal>/<workout>/delete')
def delete_workout(goal, workout):
    return render_template("delete-workout.html")

if __name__ == "__main__":
    app.secret_key = "supersupersecretkey"
    app.debug = True
    app.run(host = '0.0.0.0', port=8000)
