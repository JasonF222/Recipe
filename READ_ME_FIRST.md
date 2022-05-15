## __Bootstrap Link for Styling__
--------------
```
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
```

# __Set up Directory of Folders__

- Make sure you have your `MAIN` Directory (aka `Python Exam`)
    - `flask_app` __INSIDE__ main directory
        - `__init__.py` file goes __INSIDE__ flask_app folder!!!!
        - `config` folder
            - `mysqlconnection.py` goes here
        - `controllers` folder
            - `controller.py` files go here
        - `models` folder
            - `model.py` files go here
        - `static` folder
            - `styles.css` file goes here
        - `templates` folder
            - `html` files go here
    - `server.py` __OUTSIDE__ flask_app folder
    - `pipfile` __OUTSIDE__ flask_app folder
    - `pipfile.lock` __OUTSIDE__ flask_app folder


# __PIPENV Install Directions__

__INSIDE__ the main directory (`NOT` inside flask_app)
```
pipenv install flask PyMySQL 
```

__INSIDE__ your virtual environment
```
pipenv install flask-bcrypt
```



# __MYSQL Workbench Creating a SCHEMA__

- Go to MySQL Workbench
    - Go to `Models` (2nd Option on the __LEFT__ side)
        - Click the `+` next to Models
    - name your db
    - click `create diagram`


## __Saving Model of DB as a .mwb file for your Exam__

- in your MySQL Model* / EER Diagram db:
    - __File__ --> `Save Model As`
        - save db in your __exam folder__ as a `.mwb` file


## __REMINDER WHEN CREATING YOUR TABLES__
--------------------------

- When looking at your wireframe:
    - `Remember` to go slowly and make columns for what you see
    - `ID` should have __AI__ (Auto Increment) enabled
    - `CREATED_AT/UPDATED_AT` should have Default Expression as:
        - `Current_TIMESTAMP` for `CREATED_AT`
        - `CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP` for `UPDATED_AT`

## __WHEN SETTING UP RELATIONSHIPS BETWEEN TABLES__
--------------------------

- Make sure to choose the right relationship:
    - ` ----` relationship is generally a good option
- Once you have your relationships set up:
    - MAKE SURE YOU GO INTO EACH TABLE AND SET YOUR `IDs` TO `SINGULAR IDs`
        - (i.e `users_id` --> `user_id`)


## __When you're ready to turn your Schema into a Database__
-----------------------------

- __Database__ --> `Forward Engineer`
    - Be sure to `GENERATE DROP SCHEMA` so you have a clean db
- Once you get to `Script to be Executed` page
    - `SAVE TO FILE` and put your file as a `.sql` __INTO__ your main exam directory (i.e `Python Exam`)


# Setting up Your Templates

- __LOOK__ at your wireframe and make your `.html` files for each page of your wireframe
    - This is a good place to get your boiler plate and `CSS Bootstrap` linked up
        - Don't forget your `Titles`

# server.py & init.py set up

- __server.py__ setup:
    - import your `controllers`

    ``` 
        # Import all controllers that will be using app.routes #
        from flask_app.controllers import 'class'_controller, 'class'_controller

        # Without app server WILL NOT run #
        from flask_app import app

        if __name__ == "__main__":
            app.run(debug=True)
    ```

- __init.py__ setup:
    - import `Flask` here
```
from flask import Flask

    app = Flask(__name__)
    app.secret_key = "secretkey here"
```

- You can set up your `gobal variable` here for your db!
```
DATABASE = 'your_schema_here'
```

# controller.py files 

- `import` your dependencies at the top

```
from flask_app import app

# Import all of our features to run our app.routes #
from flask import render_template, redirect, request, session, flash

# Import all of our MODELS we will need to access for class/static methods #
from flask_app.models.'class'_model import 'Class'
from flask_app.models.'class'_model import 'Class'

# Import our Bcrypt for password hashing #
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
```

# model.py files

- `import` your dependencies at the top

```
# allows MODEL to talk to database #
from flask_app.config.mysqlconnection import connectToMySQL

# allows us to flash messages on HTML pages #
from flask import flash

# allows use of global DATABASE variable #
from flask_app import DATABASE

# allows Regular Expression for Validations #
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9._-]+.[a-zA-Z]+$')
```

