from flask import Flask, request, Response
from candy import get_candy, create_candy, delete_candy, update_candy
from users import create_user
from login import create_login, delete_login
import sys

# Intializing the flask server and CORS to allow any origin to make requests
app = Flask(__name__)

# Creating a POST request to create a new user
@app.post("/api/users")
def call_create_user():
    return create_user.signup_user()

# Created a POST request to log in users
@app.post("/api/login")
def call_create_login():
    return create_login.login_user()

# Created a DELETE request to log out users
@app.delete("/api/login")
def call_delete_login():
    return delete_login.logout_user()

# Creating a GET request to get all candy posts
@app.get("/api/candy")
def call_get_candy():
    return get_candy.get_candy_list()

# Creating a POST request to create a candy post
@app.post("/api/candy")
def call_create_candy():
    return create_candy.create_candy()

# Creating a PATCH request to edit a candy post
@app.patch("/api/candy")
def call_update_candy():
    return update_candy.edit_candy()

# Creating a DELETE request to delete a candy post
@app.delete("/api/candy")
def call_delete_candy():
    return delete_candy.delete_candy()

# Checking if an argument is given
if(len(sys.argv) > 1):
    mode = sys.argv[1]
else:
    print("No mode argument, please pass a mode argument when invoking the file")
    exit()

# Configuring the mode
if(mode == "production"):
    import bjoern  # type: ignore
    bjoern.run(app, "0.0.0.0", 5016)
elif(mode == "testing"):
    from flask_cors import CORS
    CORS(app)
    app.run(debug=True)
else:
    print("Invalid mode, please select either 'production' or 'testing'")
    exit()