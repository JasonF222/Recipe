from flask_app import app

# Import all of our features to run our app.routes #
from flask import render_template, redirect, request, session, flash

# Import all of our MODELS we will need to access for class/static methods #
from flask_app.models.user_model import User
from flask_app.models.recipe_model import Recipe


# Import our Bcrypt for password hashing #
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


# app.route for first visit page #
@app.route('/')
def index():
    # check if user is logged in #
    if 'user_id' in session:
    # if user_id is found, redirect to dashboard page #
        return redirect('/dashboard')
    return render_template('index.html')

# app.route to register user #
# DONT FORGET TO ADD YOUR POST, COMMA, and QUOTES/BRACKETS #
@app.route('/register', methods=['POST'])
def register():
# call staticmethod to check values and return true if criteria is met #
# returning True allows to continue to next check #
# if return is False, redirect to homepage and flash messages with unmet criteria #
    if not User.validate_all_present(request.form):
        return redirect ('/')
    if not User.validate_user(request.form):
        return redirect('/')
    if not User.validate_email(request.form):
        return redirect('/')
    if not User.email_exist(request.form):
        return redirect('/')
    # create a new instance of user and log it into db #
    # for security reasons, we need to hash the password before storing it! #
    pw_hash = bcrypt.generate_password_hash(request.form['pw'])
    # make a data dictionary to pass into classmethod (including our hashed password) #
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'pw_hash': pw_hash
    }
    # Now the data dictionary can safely be sent to the db (no raw password data!) #
    # Call classmethod below and send data dictionary to the db #
    # set user id to id of our new instance of user #
    user_id = User.new_user(data)
    # set session id to track successful login #
    session['user_id'] = user_id
    return redirect('/dashboard')

# app.route will check login credentials #
@app.route('/login', methods=['POST'])
def login():
    # create a data dictionary to hold submitted information #
    data = {
        'email': request.form['email']
    }
    # check database to see if email exists #
    user_in_db = User.get_by_email(data)
    # send email to classmethod and check if email exists #
    if not user_in_db:
        flash('Email is NOT registered!')
        return redirect('/')
    # check for matching passwords #
    if not bcrypt.check_password_hash(user_in_db.pw_hash, request.form['pw']):
        # if hash values DON'T match, flash message and redirect #
        flash('Invalid email or password!')
        return redirect('/')
    # set session id so we can track successful login #
    session['user_id'] = user_in_db.id
    return redirect('/dashboard')

# Dashboard app.route #
@app.route('/dashboard')
def dashboard():
    # check to make sure there has been a successful log in to render this page #
    if 'user_id' not in session:
        #if no user_id in session, that means no one has logged in or the user has logged out #
        flash('You must log in to view content!')
        return redirect('/')
    # create data dictionary to send through #
    # set the id we are sending to the db equal to the session id #
    data = {
        'id': session['user_id']
    }
    user = User.get_one(data)
    #retrieve all recipes in database #
    recipes = Recipe.get_all_recipes()
    # pass user and recipe info in on rendering html #
    return render_template('dashboard.html', user = user, recipes = recipes)

# Logout app.route #
@app.route('/logout')
def logout():
    # this will clear all of the values from the session #
    session.clear()
    return redirect('/')