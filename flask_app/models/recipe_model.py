# allows MODEL to talk to database #
from unittest import result
from flask_app.config.mysqlconnection import connectToMySQL

# allows for validations #
from flask import flash

# allows to use global variable DATABASE #
from flask_app import DATABASE

class Recipe:
    def __init__(self, data):
    # check your db table columns and line up your attributes #
        self.id = data['id']
        self.name = data['name']
        self.under_30 = data['under_30']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

# Classmethods go here #

    # This method allows us to add a recipe to the database #
    @classmethod
    def new_recipe(cls, data):
        # query is the action of talking to the db (what you would put in MySQL file in Workbench) #
        # use %()s to mogrify the data to prevent SQL injection into the db #
        query = 'INSERT INTO recipes (name, under_30, description, instructions, date_made, created_at, updated_at, user_id)'
        query += 'VALUES (%(name)s, %(under_30)s, %(description)s, %(instructions)s, %(date_made)s, NOW(), NOW(), %(user_id)s);'
        # this is the query to MySQL database to save new recipe into recipes table #
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result
    
    
    # This method allows us to edit the recipe entry #
    @classmethod
    def edit_recipe(cls, data):
        # check mogrify text to make sure it matches the column names in table #
        query = 'UPDATE recipes SET name = %(name)s, under_30 = %(under_30)s, description = %(description)s'
        query +='instructions = %(instructions)s, date_made = %(date_made)s, update_at = NOW() WHERE id = %(id)s;'
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result


    # This method allows us to get a list of dictionaries containing all recipes #
    @classmethod
    def get_all_recipes(cls):
        query = 'SELECT * FROM recipes;'
        result = connectToMySQL(DATABASE).query_db(query)
        # make an empty list to put our dictionaries into #
        recipes = []
        # check each row in table #
        for row in result:
            #for every row returned, append dictionary into recipes list #
            recipes.append(cls(row))
        # send back list of dictionaries to controller #
        return recipes


    # This method will allow us to get the info for a recipe #
    @classmethod
    def get_one_recipe(cls, data):
        query = 'SELECT * FROM recipes WHERE id = %(id)s;'
        result = connectToMySQL(DATABASE).query_db(query, data)
        # returns the first dictionary as our value #
        return cls(result[0])

    # This method will delete the recipe with the given id #
    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM recipes WHERE id = %(id)s;'
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result

    # static method for validations #

    # this will check that all fields are filled out #
    @staticmethod
    def validate_recipe_present(user):
        if not len(user['name']) > 0:
            flash('You must enter a  name!')
            return False
        if not len(user['description']) > 0:
            flash('You must enter a description!')
            return False
        if not len(user['instructions']) > 0:
            flash('You must enter instructions!')
            return False
        if not (user['date_made']):
            flash('You must enter a date made on!')
            return False
        if not user['under_30']:
            flash('You must select if this is under 30 minutes!')
            return False
        return True

    #this will check if all fields have at least 3 characters #
    @staticmethod
    def recipe_length(user):
        if not len(user['name']) > 2:
            flash('Name must be at least 3 characters!')
            return False
        if not len(user['description']) > 2:
            flash('Description must be at least 3 characters!')
            return False
        if not len(user['instructions']) > 2:
            flash('Instructions must be at least 3 characters!')
            return False
        return True
