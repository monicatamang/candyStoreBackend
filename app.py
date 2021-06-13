from flask import Flask, request, Response
import mariadb
import dbconnect
import json
import traceback
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.get("/candy")
def get_candy_list():
    conn = dbconnect.open_db_connection()
    cursor = dbconnect.create_db_cursor(conn)
    candy_list = None

    if(conn == None or cursor == None):
        print("Error in the database.")
        dbconnect.close_cursor(cursor)
        dbconnect.close_db_connection(conn)

    try:
        cursor.execute("SELECT name, description, price_in_dollars, image_url, id FROM candy")
        candy_list = cursor.fetchall()
    except:
        print("An occur has occured.")
        traceback.print_exc()

    dbconnect.close_cursor(cursor)
    dbconnect.close_db_connection(conn)

    if(candy_list == None):
        return Response("Failed to retrieve candy from the database.", mimetype="text/plain", status=500)
    else:
        candy_list_json = json.dumps(candy_list, default=str)
        return Response(candy_list_json, mimetype="application/json", status=200)