from flask import Flask, request, Response
import dbhelpers
import json

# Creating a function that gets all candy posts from the database
def get_candy_list():
    candy_list = dbhelpers.run_select_statement("SELECT c.name, c.description, c.price_in_dollars, c.image_url, c.user_id, c.id, u.username FROM users u INNER JOIN candy c ON c.user_id = u.id ORDER BY c.id DESC", [])

    # If all candy posts are not retrieved from the database, send the user a server error response
    if(candy_list == None):
        return Response("Failed to retrieve candy from the database.", mimetype="text/plain", status=500)
    # If all candy posts are retrieved from the database, convert the list of candies into JSON and send a client success response
    else:
        candy_list_json = json.dumps(candy_list, default=str)
        return Response(candy_list_json, mimetype="application/json", status=200)