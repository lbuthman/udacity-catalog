from flask import (Flask, render_template, request, redirect, url_for, flash,
jsonify)
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@app.route('/')
def home():
    return "This will display the landing page."

@app.route('/login')
def login():
    return "Provide the user a login screen"

@app.route('/<goal>')
def view_goal(goal):
    return "Returns all workouts for a certain goal."

@app.route('/<goal>/<workout>')
def view_workout(goal, workout):
    return "Retuns info for workout"

@app.route('/how-it-works')
def how_it_works():
    return "Provides info on how to use/navigate the site."

@app.route('/<goal>/new')
def new_workout(goal):
    return "Let logged in user create a new workout"

@app.route('/<goal>/<workout>/edit')
def edit_workout(goal, workout):
    return "Provides a way to edit a workout"

@app.route('/<goal>/<workout>/delete')
def delete_workout(goal, workout):
    return "Provide a way to delete a workout"

if __name__ == "__main__":
    app.secret_key = "supersupersecretkey"
    app.debug = True
    app.run(host = '0.0.0.0', port=8000)
