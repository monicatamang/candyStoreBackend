from flask import Flask, request, Response
import dbhelpers
import json
import secrets
import traceback

# Creating a function to sign up users
def signup_user():
    # Trying to get the user's username and password
    try:
        username = request.json['username']
        password = request.json['password']
        
        # If the user does not send a username or password, send a client error response
        if(username == None or username == "" or password == None or password == ""):
            return Response("Username and/or password is invalid.", mimetype="text/plain", status=400)
    except KeyError:
        traceback.print_exc()
        print("Key Error. Incorrect Key name for username or password.")
        return Response("Data Error. Invalid data was sent to the database.", mimetype="text/plain", status=400)
    except:
        traceback.print_exc()
        print("An error has occured.")
        return Response("Data Error. Invalid data was sent to the database.", mimetype="text/plain", status=400)

    # Trying to insert the user's username and password into the database
    user_id = dbhelpers.run_insert_statement("INSERT INTO users(username, password) VALUES(?, ?)", [username, password])

    # If a new id is not created for the user, send a server error response
    if(user_id == None):
        return Response("Failed to create user.", mimetype="text/plain", status=500)
    # If a new id is created for the user, create a login token and insert it into the database
    else:
        token = secrets.token_urlsafe(60)
        is_user_created = dbhelpers.run_insert_statement("INSERT INTO user_session(?, ?) VALUES(user_id, token)", [user_id, token])
        # If the login token is stored into the database, send the user's id, username and login token
        if(len(is_user_created) == 1):
            # Convert data into JSON
            signup_info = json.dumps({ 'id': user_id, 'username': username, 'loginToken': token }, default=str)
            # Send a client success response
            return Response(signup_info, mimetype="application/json", status=201)
        # If the login token is not stored into database, send server error response
        else:
            return Response("Failed to create user.", mimetype="text/plain", status=500)