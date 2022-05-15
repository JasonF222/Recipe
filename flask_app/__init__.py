# Import Flask or server WONT start #
from flask import Flask

app = Flask(__name__)

# Secret Key for cookie access allows use of session #
app.secret_key = "recipe"

# This is a global variable to use in classmethods #
DATABASE = 'recipe_db'