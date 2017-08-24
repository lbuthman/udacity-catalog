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
@app.route('/index.html/')
def index():
    categories = session.query(Category)
    exercises = session.query(Exercise).order_by(desc(Exercise.id)).limit(10).all()
    return render_template("index.html", categories=categories,
        exercises=exercises)

@app.route('/login/')
def login():
    return render_template("login.html")

@app.route('/<category>/')
def view_category(category):
    category = session.query(Category).filter_by(name=category).first()
    exercises = session.query(Exercise).filter_by(category=category).all()
    return render_template("view-category.html", category=category, exercises=exercises)

@app.route('/<category>/<exercise>/')
def view_exercise(category, exercise):
    category = session.query(Category).filter_by(name=category).first()
    exercise = session.query(Exercise).filter_by(name=exercise).first()
    return render_template("view-exercise.html", category=category,
        exercise=exercise)

@app.route('/how-it-works/')
def how_it_works():
    return render_template("how-it-works.html")

@app.route('/<category>/new/', methods=['GET', 'POST'])
def new_exercise(category):
    return render_template("new-exercise.html")

@app.route('/<category>/<exercise>/edit/', methods=['GET', 'POST'])
def edit_exercise(category, exercise):
    category = session.query(Category).filter_by(name=category).first()
    categories = session.query(Category).all()
    editedExercise = session.query(Exercise).filter_by(name=exercise).first()
    if request.method == 'POST':
        return redirect(url_for("view_exercise", category=category.name,
            exercise=editedExercise.name))
    else:
        return render_template("edit-exercise.html", category=category,
            categories=categories, exercise=editedExercise)

@app.route('/<category>/<exercise>/delete/', methods=['GET', 'POST'])
def delete_exercise(category, exercise):
    return render_template("delete-exercise.html")

def get_category(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    return category.name

app.jinja_env.globals.update(get_category=get_category)

if __name__ == "__main__":
    app.secret_key = "supersupersecretkey"
    app.debug = True
    app.run(host = '0.0.0.0', port=8000)
