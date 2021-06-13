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

@app.post("/candy")
def create_candy():
    try:
        candy_name = str(request.json['name'])
        candy_description = str(request.json['description'])
        candy_price = float(request.json['priceInDollars'])
        candy_image = str(request.json['imageUrl'])

    except:
        print("Invalid data being passed to the database.")
        traceback.print_exc()
        return Response("Invalid data being passed to the database.", mimetype="text/plain", status=400)

    conn = dbconnect.open_db_connection()
    cursor = dbconnect.create_db_cursor(conn)
    new_id = -1

    if(conn == None or cursor == None):
        print("Error in the database.")
        dbconnect.close_cursor(cursor)
        dbconnect.close_db_connection(conn)

    try:
        cursor.execute("INSERT INTO candy(name, description, price_in_dollars, image_url) VALUES(?, ?, ?, ?)", [candy_name, candy_description, candy_price, candy_image])
        conn.commit()
        new_id = cursor.lastrowid
    except:
        print("An occur has occured.")
        traceback.print_exc()

    dbconnect.close_cursor(cursor)
    dbconnect.close_db_connection(conn)

    if(new_id == -1):
        return Response("Failed to create a new candy.", mimetype="text/plain", status=500)
    else:
        new_candy_json = json.dumps([new_id, candy_name, candy_description, candy_price, candy_image], default=str)
        return Response(new_candy_json, mimetype="application/json", status=201)

@app.delete("/candy")
def delete_candy():
    try:
        candy_id = int(request.json['id'])
    except:
        print("Invalid data being passed to the database.")
        traceback.print_exc()
        return Response("Invalid data being passed to the database.", mimetype="text/plain", status=400)

    conn = dbconnect.open_db_connection()
    cursor = dbconnect.create_db_cursor(conn)
    row_count = 0

    if(conn == None or cursor == None):
        print("Error in the database.")
        dbconnect.close_cursor(cursor)
        dbconnect.close_db_connection(conn)

    try:
        cursor.execute("DELETE FROM candy WHERE id = ?", [candy_id])
        conn.commit()
        row_count = cursor.rowcount
    except:
        print("An occur has occured.")
        traceback.print_exc()

    dbconnect.close_cursor(cursor)
    dbconnect.close_db_connection(conn)

    if(row_count == 1):
        return Response("Candy was successfully deleted.", mimetype="application/json", status=200)
    else:
        return Response("Failed to delete candy.", mimetype="text/plain", status=500)

app.run(debug=True)