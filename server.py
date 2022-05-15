# Import all controllers that will be using app.routes #
from flask_app.controllers import user_controller, recipe_controller

# Without app server WILL NOT run #
from flask_app import app

if __name__ == "__main__":
    app.run(debug=True)