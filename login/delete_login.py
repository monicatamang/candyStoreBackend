from flask import Flask, request, Response
import dbhelpers
import traceback

# Creating a function that logs out a user
def logout_user():
    # Trying to get the user's login token
    try:
        login_token = request.json['loginToken']
    except KeyError:
        traceback.print_exc()
        print("Key Error. Incorrect Key name for the username or password.")
        return Response("Username and password do not match the database records.", mimetype="text/plain", status=400)
    except:
        traceback.print_exc()
        print("An error has occured.")
        return Response("Username and password do not match the database records.", mimetype="text/plain", status=400)

    # Trying to delete the user's login token from the database
    row_count = dbhelpers.run_delete_statement("DELETE FROM user_session WHERE token = ?", [login_token,])

    # If the user's login token is deleted from the database, send a client success response
    if(row_count == 1):
        return Response(status=204)
    # If the user's login token is not deleted from the database, send a server error response
    else:
        return Response("Failed to log out.", mimetype="text/plain", status=500)