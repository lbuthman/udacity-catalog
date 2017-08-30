from flask import (
    Flask, render_template, request, redirect, url_for, flash, jsonify)
from flask import session
from flask import make_response
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Exercise, User
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import random
import string
import json
import httplib2
import requests

CLIENT_ID = json.loads(
            open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Exercise Catalog"

app = Flask(__name__)

engine = create_engine('sqlite:///exercisecatalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
db_session = DBSession()


# Create anti-forgery state token
@app.route('/login/')
def login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    session['state'] = state
    return render_template("login.html", STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    str_response = h.request(url, 'GET')[1].decode('utf-8')
    result = json.loads(str_response)

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = session.get('access_token')
    stored_gplus_id = session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
                    json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    session['access_token'] = credentials.access_token
    session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    session['provider'] = 'google'
    session['username'] = data['name']
    session['email'] = data['email']
    # session['picture'] = data['picture']
    user_id = get_user_id(session['email'])
    if not user_id:
        user_id = create_user(session)
    session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += session['username']
    output += '!</h1>'
    flash("You are in! Feel free to add, edit or delete exercises.".format(
        session['username']), "success")
    return output


def gdisconnect():
    access_token = session.get('access_token')
    if access_token is None:
        print('Access Token is None')
        response = make_response(
                    json.dumps('Current user is not connected'), 401)
        response.headers['Content-Type'] = 'application/json'
        flash("Current user is not connected", "warning")
        return response

    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % (
            session['access_token'])
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(
                    json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        flash("Failed to revoke token for given user", "danger")
        return response


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    # Validate state token
    if request.args.get('state') != session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Obtain authorization code
    access_token = request.data
    access_token = access_token.decode("utf-8")

    app_id = json.loads(
                open('fb_client_secrets.json', 'r').read())['web']['app_id']
    app_secret = json.loads(
                open(
                    'fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = ('https://graph.facebook.com/v2.10/oauth/access_token?'
           'grant_type=fb_exchange_token&client_id=%s&client_secret=%s'
           '&fb_exchange_token=%s') % (app_id, app_secret, access_token)

    h = httplib2.Http()
    str_response = h.request(url, 'GET')[1].decode('utf-8')
    data = json.loads(str_response)

    # Extract the access token from response
    token = 'access_token=' + data['access_token']

    url = "https://graph.facebook.com/v2.10/me?%s&fields=name,id,email" % token
    h = httplib2.Http()
    str_response = h.request(url, 'GET')[1].decode('utf-8')
    data = json.loads(str_response)

    session['provider'] = 'facebook'
    session['username'] = data['name']
    session['email'] = data['email']
    session['facebook_id'] = data['id']
    session['access_token'] = token

    user_id = get_user_id(session['email'])
    if not user_id:
        user_id = create_user(session)
    session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += session['username']
    output += '!</h1>'
    flash("You are in! Feel free to add, edit or delete exercises.".format(
        session['username']), "success")
    return output


def fbdisconnect():
    facebook_id = session['facebook_id']
    access_token = session['access_token']
    url = "https://graph.facebook.com/%s/permissions?access_token=%s" % (
        facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "success"


@app.route('/disconnect')
def disconnect():
    if 'provider' in session:
        if session['provider'] == 'google':
            gdisconnect()
            del session['access_token']
            del session['gplus_id']
        if session['provider'] == 'facebook':
            fbdisconnect()
            del session['facebook_id']
        del session['username']
        del session['email']
        del session['user_id']
        del session['provider']
        flash("You have been Successfully disconnected", "success")
        return redirect(url_for("index"))
    else:
        flash("You were never logged in (never even here, creepy.)", "warning")
        return redirect(url_for("index"))


@app.route('/categories/JSON/')
def all_categoriesJSON():
    categories = db_session.query(Category).all()
    return jsonify(Categories=[c.serialize for c in categories])


@app.route('/exercises/JSON/')
def all_exercisesJSON():
    exercises = db_session.query(Exercise).order_by(desc(Exercise.id)).all()
    return jsonify(Exercises=[e.serialize for e in exercises])


@app.route('/<category>/exercises/JSON/')
def category_exercisesJSON(category):
    category = db_session.query(Category).filter_by(name=category).one()
    exercises = db_session.query(Exercise).filter_by(category=category).all()
    return jsonify(CategoryExercises=[e.serialize for e in exercises])


@app.route('/<category>/<exercise>/JSON/')
def one_exerciseJSON(category, exercise):
    category = db_session.query(Category).filter_by(name=category).one()
    exercise = db_session.query(
                Exercise).filter_by(name=exercise, category=category).one()
    return jsonify(Exercise=[exercise.serialize])


@app.route('/')
@app.route('/index.html/')
def index():
    categories = db_session.query(Category)
    exercises = db_session.query(
                Exercise).order_by(desc(Exercise.id)).limit(10).all()
    return render_template(
            "index.html", categories=categories, exercises=exercises)


@app.route('/<category>/')
def view_category(category):
    category = db_session.query(Category).filter_by(name=category).first()
    exercises = db_session.query(Exercise).filter_by(category=category).all()
    return render_template(
            "view-category.html", category=category, exercises=exercises)


@app.route('/<category>/<exercise>/')
def view_exercise(category, exercise):
    category = db_session.query(Category).filter_by(name=category).first()
    exercise = db_session.query(Exercise).filter_by(name=exercise).first()
    if session['user_id'] == exercise.user_id:
        return render_template(
                "view-exercise.html", category=category, exercise=exercise)
    else:
        return render_template(
                "publicview-exercise.html", category=category,
                exercise=exercise)


@app.route('/how-it-works/')
def how_it_works():
    return render_template("how-it-works.html")


@app.route('/<category>/new/', methods=['GET', 'POST'])
def new_exercise(category):
    if 'username' not in session:
        return redirect('/login')
    category = db_session.query(Category).filter_by(name=category).first()
    name = ""
    description = ""
    url = ""
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        url = request.form['url']
        if name == "" or description == "" or url == "":
            flash(
                "All fields are required. Please check and try again",
                'danger')
            return render_template(
                    "new-exercise.html", category=category,
                    name=name, description=description, url=url)
        elif "embed" not in url:
            flash("""Uh oh! Double check the url and make sure you use the
                    embedded version.""", 'warning')
            return render_template(
                    "new-exercise.html", category=category,
                    name=name, description=description, url=url)
        else:
            newExercise = Exercise(
                            name=name, description=description, url=url,
                            category=category, user_id=session['user_id'])
            db_session.add(newExercise)
            db_session.commit()
            flash("Sweet to the beat! You successful added an exercise!")
            return redirect(url_for("view_category", category=category.name))
    else:
        return render_template(
            "new-exercise.html", category=category, name=name,
            description=description, url=url)


@app.route('/<category>/<exercise>/edit/', methods=['GET', 'POST'])
def edit_exercise(category, exercise):
    if 'username' not in session:
        return redirect('/login')
    category = db_session.query(Category).filter_by(name=category).first()
    categories = db_session.query(Category).all()
    editedExercise = db_session.query(
                        Exercise).filter_by(name=exercise).first()

    if session['user_id'] != editedExercise.user_id:
        flash(
            "Sorry, you don't have permission to edit that exercise.",
            "danger")
        return redirect(url_for("index"))

    if request.method == 'POST':
        editedExercise.name = request.form['name']
        editedExercise.description = request.form['description']
        editedExercise.url = request.form['url']
        flash("Exercise {} has been edited.".format(editedExercise.name))
        return redirect(url_for(
                "view_exercise", category=category.name,
                exercise=editedExercise.name))
    else:
        return render_template(
                "edit-exercise.html", category=category,
                categories=categories, exercise=editedExercise)


@app.route('/<category>/<exercise>/delete/', methods=['GET', 'POST'])
def delete_exercise(category, exercise):
    if 'username' not in session:
        return redirect('/login')
    category = db_session.query(Category).filter_by(name=category).first()
    deletedExercise = db_session.query(
                        Exercise).filter_by(name=exercise).first()

    if session['user_id'] != deletedExercise.user_id:
        flash(
            "Sorry, you don't have permission to delete that exercise.",
            "danger")
        return redirect(url_for("index"))

    if request.method == 'POST':
        db_session.delete(deletedExercise)
        db_session.commit()
        flash("Exercise {} has been deleted.".format(deletedExercise.name))
        return redirect(url_for("view_category", category=category.name))
    else:
        return render_template(
                "delete-exercise.html", category=category,
                exercise=deletedExercise)


def get_category(category_id):
    """Returns the name of a category for a given category ID."""
    category = db_session.query(Category).filter_by(id=category_id).one()
    return category.name


# Add the get_category() method to jinja template's global environment
app.jinja_env.globals.update(get_category=get_category)


def get_user_id(email):
    """Returns the user id for a given user's email address if exists."""
    try:
        user = db_session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


def get_user_info(user_id):
    """Returns the user for a given user's id if exists."""
    try:
        user = db_session.query(User).filter_by(id=user_id).one()
        return user
    except:
        return None


def create_user(session):
    """Adds new user to Database and returns the user's id."""
    newUser = User(name=session['username'], email=session['email'])
    db_session.add(newUser)
    db_session.commit()
    user = db_session.query(User).filter_by(email=session['email']).one()
    return user.id


if __name__ == "__main__":
    app.secret_key = "supersupersecretkey"
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
