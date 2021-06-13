from flask import Flask, request, Response
import mariadb
import dbconnect
import json
import traceback
from flask_cors import CORS

# Intializing the flask server and CORS to allow any origin to make requests
app = Flask(__name__)
CORS(app)

# Creating a function that closes the database connection and the cursor
def close_db_connection_and_cursor(conn, cursor):
    # Closing the cursor and database connection
    closing_cursor = dbconnect.close_cursor(cursor)
    closing_db = dbconnect.close_db_connection(conn)
    # If the cursor or database connection failed to close, print an error message
    if(closing_cursor == False or closing_db == False):
        print("Failed to close cursor and database connection.")

# Checking to see if the database connection is opened and the cursor is created
def check_db_connection_and_cursor(conn, cursor):
    # If the connection was successful but the cursor was failed to be created, print an error message and attempt to close the cursor and database connection again
    if(conn == None or cursor == None):
        print("An error has occured in the database.")
        dbconnect.close_cursor(cursor)
        dbconnect.close_db_connection(conn)
        return

# Creating a GET request to the "candy" endpoint to get all candies
@app.get("/candy")
def get_candy_list():
    # Opening the database and creating a cursor
    conn = dbconnect.open_db_connection()
    cursor = dbconnect.create_db_cursor(conn)

    # Initializing the candy list and assigning it a value so that it can still be referenced after the try-except block
    candy_list = None

    # Checking to see if the database connection is opened and whether the cursor is created
    check_db_connection_and_cursor(conn, cursor)

    # Creating a try-except block to catch errors when getting all candies from the database
    try:
        # Getting the all candies from the database
        cursor.execute("SELECT name, description, price_in_dollars, image_url, id FROM candy")
        candy_list = cursor.fetchall()
    # Raising the OperationalError exception for things that are not in control of the programmer, printing an error message and the traceback
    except mariadb.OperationalError:
        traceback.print_exc()
        print("An operational error has occured when retrieving the all candies from the database.")
    # Raising the ProgrammingError exception for errors made by the programmer, printing an error message and the traceback
    except mariadb.ProgrammingError:
        traceback.print_exc()
        print("Invalid SQL syntax.")
    # Raising the DatabaseError exception for errors related to the database, printing an error message and the traceback
    except mariadb.DatabaseError:
        traceback.print_exc()
        print("Errors detected in the database and resulted in a connection failure.")
    # Raising a general exception to catch all other errors, printing a general error message and the traceback
    except:
        traceback.print_exc()
        print("An error has occured.")

    # Closing the cursor and database connection
    close_db_connection_and_cursor(conn, cursor)

    # If all candies were not retrieved from the database, send the user a server error response
    if(candy_list == None):
        return Response("Failed to retrieve candy from the database.", mimetype="text/plain", status=500)
    # If all candies were successfully retrieved from the database, convert the list of candies into JSON format and send a client success response
    else:
        candy_list_json = json.dumps(candy_list, default=str)
        return Response(candy_list_json, mimetype="application/json", status=200)

# Creating a POST request to the "candy" endpoint to create a candy
@app.post("/candy")
def create_candy():
    # Creating a try-except block to catch errors when receiving the user's data
    try:
        # Converting the user's data into their appropriate data types
        candy_name = request.json.get('name')
        candy_description = request.json.get('description')
        candy_price = float(request.json.get('priceInDollars'))
        candy_image = request.json.get('imageUrl')

        # Placing the if statements in the try-except block so that in the case where one of the lines above fail to run, the errors will be "caught" by the exceptions
        # If the candy name or price is not provided by the user, send a client error response
        if(candy_name == None or candy_price == None):
            return Response("Data Error. Invalid data was sent to the database.", mimetype="text/plain", status=400)
        
        # If the user creates a candy without adding content to the description, set the description as an empty string
        if(candy_description == None or candy_description == ""):
            candy_description = ""
        
        # If the user creates a candy without adding a image URL, set the image URL as an empty string
        if(candy_image == None or candy_image == ""):
            candy_image = ""
    # Raising the UnboundLocalError exception if one or more variables don't exist due to invalid data being sent to the database
    except UnboundLocalError:
        traceback.print_exc()
        print("Data Error. Referencing variables that are not declared.")
    # Raising the ValueError exception if the user sends data with inappropriate data types, printing an error message and the traceback
    except ValueError:
        traceback.print_exc()
        print("Invalid data was sent to the database.")
    # Raising a general exception to catch all other errors, printing a general error message and the traceback
    except:
        traceback.print_exc()
        print("An error has occured.")
        # Sending the user a client error response and stopping the function from running the next lines of code that interacts with the database
        return Response("Data Error. Invalid data was sent to the database.", mimetype="text/plain", status=400)

    # If the user sends valid data, open the database connection and create a cursor
    conn = dbconnect.open_db_connection()
    cursor = dbconnect.create_db_cursor(conn)

    # Assign the new id of the candy to be a negative number which indicates that a new id was not created
    new_id = -1

    # Checking to see if the database connection is opened and whether the cursor is created
    check_db_connection_and_cursor(conn, cursor)

    # Creating a try-except block to catch errors when inserting the new candy into the database
    try:
        # Inserting the new candy into the database and commiting the changes
        cursor.execute("INSERT INTO candy(name, description, price_in_dollars, image_url) VALUES(?, ?, ?, ?)", [candy_name, candy_description, candy_price, candy_image])
        conn.commit()

        # Getting the id of new candy
        new_id = cursor.lastrowid
    # Raising an IntegrityError exception if the user sends a candy name that already exists in the database, printing an error message and the traceback
    except mariadb.IntegrityError:
        traceback.print_exc()
        print(f"Unique key constraint failure. {candy_name} already exists in the database.")
    # Raising the OperationalError exception for things that are not in control of the programmer, printing an error message and the traceback
    except mariadb.OperationalError:
        traceback.print_exc()
        print(f"An operational error has occured when creating {candy_name}.")
    # Raising the ProgrammingError exception for errors made by the programmer, printing an error message and the traceback
    except mariadb.ProgrammingError:
        traceback.print_exc()
        print("Invalid SQL syntax.")
    # Raising the DatabaseError exception for errors related to the database, printing an error message and the traceback
    except mariadb.DatabaseError:
        traceback.print_exc()
        print(f"An error in the database has occured. Failed to create {candy_name}.")
    # Raising a general exception to catch all other errors, printing a general error message and the traceback
    except:
        traceback.print_exc()
        print("An error has occured.")
    
    # Closing the cursor and database connection
    close_db_connection_and_cursor(conn, cursor)

    # If the new id was not created, send the user a client error response
    if(new_id == -1):
        return Response("Failed to create a new candy.", mimetype="text/plain", status=500)
    # If the new id was created, send the user the new candy in JSON format and a client success response
    else:
        new_candy_json = json.dumps([candy_name, candy_description, candy_price, candy_image, new_id], default=str)
        return Response(new_candy_json, mimetype="application/json", status=201)

# Creating a DELETE request to the "candy" endpoint to delete an exisiting candy
@app.delete("/candy")
def delete_candy():
    # Creating a try-except block to catch errors when receiving the candy id sent by the user
    try:
        # Converting the id into an integer data type
        candy_id = int(request.json['id'])
    # Raising an IndexError exception if the user enters an id that does not exist in the database
    except IndexError:
        traceback.print_exc()
        print("The candy id of does not exist in the database.")
    # Raising the ValueError exception if the user sends an id that has a data type other than an integer, printing an error message and the traceback
    except ValueError:
        traceback.print_exc()
        print("Invalid data was sent to the database.")
    # Raising a general exception to catch all other errors, printing a general error message and the traceback
    except:
        traceback.print_exc()
        print("An error has occured.")
        # Sending the user a client error response and stopping the function for running the next lines of code that interacts with the database
        return Response("Invalid data was sent to the database.", mimetype="text/plain", status=400)

    # If the user sends a valid id, open the database connection and create a cursor
    conn = dbconnect.open_db_connection()
    cursor = dbconnect.create_db_cursor(conn)

    # Initializing the row count and assigning it a value so that it can still be referenced after the try-except block
    row_count = 0

    # Checking to see if the database connection is opened and whether the cursor is created
    check_db_connection_and_cursor(conn, cursor)

    # Creating a try-except block to catch errors when deleting a candy from the database
    try:
        # Deleting a candy from the database and committing the changes
        cursor.execute("DELETE FROM candy WHERE id = ?", [candy_id])
        conn.commit()

        # Getting the number of rows that have been deleted from the database
        row_count = cursor.rowcount
    # Raising the OperationalError exception for things that are not in control of the programmer, printing an error message and the traceback
    except mariadb.OperationalError:
        traceback.print_exc()
        print(f"An operational error has occured. Failed to delete candy with an id of {candy_id} in the database.\n")
    # Raising the ProgrammingError exception for errors made by the programmer, printing an error message and the traceback
    except mariadb.ProgrammingError:
        traceback.print_exc()
        print("Invalid SQL syntax.")
    # Raising the DatabaseError exception for errors related to the database, printing an error message and the traceback
    except mariadb.DatabaseError:
        traceback.print_exc()
        print(f"An error in the database has occured. Failed to delete candy with an id of {candy_id} in the database.")
    # Raising a general exception to catch all other errors, printing a general error message and the traceback
    except:
        traceback.print_exc()
        print("An error has occured.")

    # Closing the cursor and database connection
    close_db_connection_and_cursor(conn, cursor)

    # If the database successfully deleted the candy, send a client success response
    if(row_count == 1):
        return Response(f"Candy with an id of {candy_id} was deleted.", mimetype="application/json", status=200)
    # If the database failed to delete the candy, send a server error response
    else:
        return Response("Failed to delete candy.", mimetype="text/plain", status=500)

# Creating a PATCH request to the "candy" endpoint to edit a candy
@app.patch("/candy")
def edit_candy():
    # Opening the database and creating a cursor
    conn = dbconnect.open_db_connection()
    cursor = dbconnect.create_db_cursor(conn)

    # Initalizing the unedited candy as a variable and assigning it a value of "None" so that it can still be referenced after the try-except block
    old_candy = None

    # Checking to see if the database connection is opened and whether the cursor is created
    check_db_connection_and_cursor(conn, cursor)
    
    # Creating a try-except block to catch errors when getting all the old candies from the database
    try:
        # Converting the candy id into an integer and getting the unedited candy from the database
        candy_id = int(request.json['id'])
        cursor.execute("SELECT name, description, price_in_dollars, image_url, id FROM candy WHERE id = ?", [candy_id])
        old_candy = cursor.fetchall()
    # Raising an IndexError exception if the user enters an id that does not exist in the database
    except IndexError:
        traceback.print_exc()
        print(f"The candy id of {candy_id} does not exist in the database.")
    # Raising the ValueError exception if the user sends an id that has a data type other than an integer, printing an error message and the traceback
    except ValueError:
        traceback.print_exc()
        print("Invalid data was sent to the database.")
    # Raising a general exception to catch all other errors, printing a general error message and the traceback
    except:
        print("An error has occured.")
        traceback.print_exc()
        # If the database failed to delete the candy, send a client error response
        return Response("Invalid data was sent to the database.", mimetype="text/plain", status=400)

    # Closing the cursor and database connection
    close_db_connection_and_cursor(conn, cursor)

    # If the candy id was invalid or the list of old candies could not be retrieved from the database, send a client server error
    if(candy_id == None or old_candy == None):
        return Response("Invalid data being passed to the database.", mimetype="text/plain", status=400)

    # Creating a try-except block to catch errors when updating a candy
    try:
        # Receiving the user's data
        candy_name = request.json.get('name')
        candy_description = request.json.get('description')
        candy_price = request.json.get('priceInDollars')
        candy_image = request.json.get('imageUrl')

        # If the database contains the old candy name with valid content but the user updates the name without content, set the name to the old candy name
        if((old_candy[0][0] != None or old_candy[0][0] != "") and (candy_name == None or candy_name == "")):
            candy_name = old_candy[0][0]

        # If the database contains the old candy description with valid content but the user updates the description without content, set the description to the old candy description
        if((old_candy[0][1] != None or old_candy[0][1] != "") and (candy_description == None or candy_description == "")):
            candy_description = old_candy[0][1]
        # If the database contains the old candy description which initially had no content and the user has not updated the new description with content, set the description as an empty string
        elif((old_candy[0][1] == None or old_candy[0][1] == "") and (candy_description == None or candy_description == "")):
            candy_description == ""

        # If the database contains the old candy price with valid content but the user updates the price without content, set the price to the old candy price
        if((old_candy[0][2] != None or old_candy[0][2] != "") and (candy_price == None or candy_price == "")):
            candy_price = old_candy[0][2]
        
        # If the database contains the old candy image with valid content but the user updates the image without content, set the image to the old candy image
        if((old_candy[0][3] != None or old_candy[0][3] != "") and (candy_image == None or candy_image == "")):
            candy_image = old_candy[0][3]
        # If the database contains the old candy image which initially had no content and the user has not updated the new image with content, set the image as an empty string
        elif((old_candy[0][3] == None or old_candy[0][3] == "") and (candy_image == None or candy_image == "")):
            candy_image == ""
    # Raising the UnboundLocalError exception if one or more variables don't exist due to invalid data being sent to the database
    except UnboundLocalError:
        traceback.print_exc()
        print("Data Error. Referencing variables that are not declared.")
    # Raising the ValueError exception if the user sends data with inappropriate data types, printing an error message and the traceback
    except ValueError:
        traceback.print_exc()
        print("Invalid data was sent to the database.")
    # Raising a general exception to catch all other errors, printing a general error message and the traceback
    except:
        traceback.print_exc()
        print("An error has occured.")
        # Sending the user a client error response and stopping the function from running the next lines of code that interacts with the database
        return Response("Data Error. Invalid data was sent to the database.", mimetype="text/plain", status=400)
    
    # If the user sends valid data, open the database connection and create a cursor 
    conn = dbconnect.open_db_connection()
    cursor = dbconnect.create_db_cursor(conn)

    # Initializing the row count and assigning it a value so that it can still be referenced after the try-except block
    row_count = 0

    # Checking to see if the database connection is opened and whether the cursor is created
    check_db_connection_and_cursor(conn, cursor)

    # Creating a try-except block to catch errors when updating the candy to the database
    try:
        # Replacing the edited candy with the old candy and commiting the changes
        cursor.execute("UPDATE candy SET name = ?, description = ?, price_in_dollars = ?, image_url = ? WHERE id = ?", [candy_name, candy_description, candy_price, candy_image, candy_id])
        conn.commit()

        # Getting the number of rows that have been updated in the database
        row_count = cursor.rowcount
    # Raising the OperationalError exception for things that are not in control of the programmer, printing an error message and the traceback
    except mariadb.OperationalError:
        traceback.print_exc()
        print(f"An operational error has occured. Failed to update {candy_name} to the database.")
    # Raising the ProgrammingError exception for errors made by the programmer, printing an error message and the traceback
    except mariadb.ProgrammingError:
        traceback.print_exc()
        print("Invalid SQL syntax.")
    # Raising the DatabaseError exception for errors related to the database, printing an error message and the traceback
    except mariadb.DatabaseError:
        traceback.print_exc()
        print(f"An error in the database has occured. Failed to update {candy_name} to the database.")
    # Raising a general exception to catch all other errors, printing a general error message and the traceback
    except:
        traceback.print_exc()
        print("An error has occured.")

    # Closing the cursor and database connection
    close_db_connection_and_cursor(conn, cursor)

    # If the edited candy was successfully stored into the database, send the user the edited candy in JSON format and a client success response
    if(row_count == 1):
        edited_candy_json = json.dumps([candy_name, candy_description, candy_price, candy_image, candy_id], default=str)
        return Response(edited_candy_json, mimetype="application/json", status=200)
    # If the database failed to store the edited candy, send the user a server error response
    else:
        return Response("Failed to edit candy.", mimetype="text/plain", status=500)

# Running the flask server with debug mode turned on
app.run(debug=True)