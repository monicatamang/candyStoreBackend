from flask import Flask, request, Response
import dbhelpers
import traceback

# Creating a function that deletes a candy post
def delete_candy():
    # Trying to get the user's login token and candy id
    try:
        login_token = request.json['loginToken']
        candy_id = int(request.json['candyId'])
    except KeyError:
        traceback.print_exc()
        print("Key Error. Incorrect Key name of data.")
        return Response("Invalid data was sent to the database. Failed to delete candy.", mimetype="text/plain", status=400)
    except:
        traceback.print_exc()
        print("An error has occured.")
        return Response("Invalid data was sent to the database. Failed to delete candy.", mimetype="text/plain", status=400)

    # Trying to delete a candy post from the database
    row_count = dbhelpers.run_delete_statement("DELETE c FROM candy c INNER JOIN user_session us ON us.user_id = c.user_id WHERE us.token = ? AND c.id = ?", [login_token, candy_id])

    # If the candy post is deleted from the database, send a client success response
    if(row_count == 1):
        return Response(status=204)
    # If the candy post is not deleted from database, send a server error response
    else:
        return Response("Failed to delete candy.", mimetype="text/plain", status=500)