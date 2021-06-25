from flask import Flask, request, Response
import dbhelpers
import secrets
import json
import traceback

# Creating a function that logs in a user
def login_user():
    # Trying to get the user's username and password
    try:
        username = request.json['username']
        password = request.json['password']
    except KeyError:
        traceback.print_exc()
        print("Key Error. Incorrect Key name for the username or password.")
        return Response("Username and password do not match the database records.", mimetype="text/plain", status=400)
    # Raising a general exception to catch all other errors, printing a general error message, the traceback and a client error response
    except:
        traceback.print_exc()
        print("An error has occured.")
        return Response("Username and password do not match the database records.", mimetype="text/plain", status=400)

    # Checking to see if the username and password given matches the database records
    user_info = dbhelpers.run_select_statement("SELECT username, password, id FROM users WHERE username = ? AND password = ?", [username, password])

    # If the usename and password matches, create a login token and try inserting into the database
    if(len(user_info) == 1):
        token = secrets.token_urlsafe(60)
        is_user_logged_in = dbhelpers.run_insert_statement("INSERT INTO user_session(user_id, token) VALUES(?, ?)", [user_info[0][2], token])
        # If the login token is not stored in the database, send a server error response
        if(is_user_logged_in == None):
            return Response("Failed to log in.", mimetype="text/plain", status=500)
        # If the loging token is stored in the database, send a client success response with the user's id and username as JSON
        else:
            login_info = json.dumps({ 'id': user_info[0][2], 'username': user_info[0][0] }, default=str)
            return Response(login_info, mimetype="application/json", status=200)
    # If the username and password do not match, send a server error response
    else:
        return Response("Username and/or password does not match our records.", mimetype="text/plain", status=500)