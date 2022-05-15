from flask_app import app

# Import all of our features to run our app.routes #
from flask import render_template, redirect, request, session, flash

# Import all of our MODELS we will need to access for class/static methods #
from flask_app.models.user_model import User
from flask_app.models.recipe_model import Recipe


# This method is for the recipe edit #
@app.route('/edit_recipe/<int:recipe_id>')
def edit_recipe(recipe_id):
    if 'user_id' not in session:
        flash('You must be logged in or registered to view content!')
        return redirect('/')

    data = {
        'id': recipe_id
    }
    
    recipe = Recipe.get_one_recipe(data)
    return render_template('edit_recipe.html', recipe = recipe)

@app.route('/send_edit/<int:id>', methods=['POST'])
def send_edit(id):
    # to validate all fields are filled out #
    if not Recipe.validate_recipe_present(request.form):
        return redirect(f'/edit_recipe/{id}')
    # to validate that all fields have at least 3 characters #
    if not Recipe.recipe_length(request.form):
        return redirect(f'/edit_recipe/{id}')
    # if validation is passed, we can send this to the db! #
    # need a data dictionary to pass recipe id in #
    data = {

        'id': id,
        'name': request.form['name'],
        'under_30': request.form['under_30'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'date_made': request.form['date_made']
    }
    Recipe.edit_recipe(data)
    # after recipe has been edited, redirect to dashboard #
    return redirect('/dashboard')

# This method is for our create recipe #
@app.route('/create_recipe')
def create_recipe():
    # to check if user is logged in #
    if 'user_id' not in session:
        flash('You must register or log in to view content!')
        return redirect('/')
    # we need to pass user id through so new recipes have a creator #
    user_id = session['user_id']
    return render_template('new_recipe.html', user_id = user_id)

# This method is for our new recipe #
@app.route('/new_recipe', methods=['POST'])
def submit_new():
    # to validate all fields are filled out
    if not Recipe.validate_recipe_present(request.form):
        return redirect('/new_recipe')
    # to validate that all fields have at least 3 characters #
    if not Recipe.recipe_length(request.form):
        return redirect('/new_recipe')
    # if the form passes validation, we can send to the database #
    Recipe.new_recipe(request.form)
    # after we have created the new recipe, we redirect to dashboard #
    return redirect('/dashboard')

# This method is for our show recipe #
@app.route('/show_recipe/<int:id>')
def show_recipe(id):
    # check if user is logged in #
    if 'user_id' not in session:
        flash('You must register or log in to view this content!')
        return redirect('/')
    # we need to get the recipe information that we have passed through the id from the url #
    data = {
        'id': id
    }
    #we call the classmethod to get the dictionary for the id and set a variable to pass through #
    recipe = Recipe.get_one_recipe(data)
    # we pass the data to the html to render the recipe information #
    # we need to get the user data to display correct name #
    # use variable to pass user info into dictionary to the html #
    data = {
        'id': session['user_id']
    }
    user = User.get_one(data)
    return render_template('show_recipe.html', recipe = recipe, user = user)

# this method is to delete a recipe #
@app.route('/delete_recipe/<int:id>')
def delete_recipe(id):
    # this classmethod is being called to delete the recipe from the database #
    # we are using a data dictionary to pass id to database #
    data = {
        'id': id
    }
    # This method sends the delete function to the database #
    Recipe.delete(data)
    return redirect('/dashboard')

    