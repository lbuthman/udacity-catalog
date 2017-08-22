from flask import (Flask, render_template, request, redirect, url_for, flash,
jsonify)
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Exercise
import random, string
import json
import requests

app = Flask(__name__)

engine = create_engine('sqlite:///exercisecatalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/index.html')
@app.route('/index.html/')
def index():
    categories = session.query(Category)
    exercises = session.query(Exercise).order_by(desc(Exercise.id))
    return render_template("index.html", categories=categories,
        exercises=exercises)

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
    return "category name"

app.jinja_env.globals.update(get_category=get_category)

if __name__ == "__main__":
    app.secret_key = "supersupersecretkey"
    app.debug = True
    app.run(host = '0.0.0.0', port=8000)
