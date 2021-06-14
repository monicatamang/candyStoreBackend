from flask import Flask, request, Response
import mariadb
import dbconnect
import json
import traceback
from flask_cors import CORS

# Creating a function that closes the database connection and the cursor
def close_db_connection_and_cursor(conn, cursor):
    # Closing the cursor and database connection
    closing_cursor = dbconnect.close_cursor(cursor)
    closing_db = dbconnect.close_db_connection(conn)
    # If the cursor or database connection failed to close, print an error message
    if(closing_cursor == False or closing_db == False):
        print("Failed to close cursor and database connection.")

# Checking to see if the database connection is opened and whether the cursor is created
def check_db_connection_and_cursor(conn, cursor):
    # If the connection was successful but the cursor was failed to be created, print an error message and attempt to close the cursor and database connection again
    if(conn == None or cursor == None):
        print("An error has occured in the database.")
        dbconnect.close_cursor(cursor)
        dbconnect.close_db_connection(conn)
        return

# Intializing the flask server and CORS to allow any origin to make requests
app = Flask(__name__)
CORS(app)

# Creating a POST request to the "users" endpoint to create a new account for users
@app.post("/users")
def create_user():
    # Creating a try-except block to catch errors when users sign up
    try:
        # Receiving the user's username and password and storing it as a variable
        username = request.json['username']
        password = request.json['password']
        
        # If the username or password is not provided by the user, send a client error response
        if(username == None or username == "" or password == None or password == ""):
            return Response("Data Error. Invalid data was sent to the database.", mimetype="text/plain", status=400)
    # Raising the KeyError exception if the user sends data with the incorrect key names, printing an error message and the traceback
    except KeyError:
        traceback.print_exc()
        print("Key Error. Incorrect Key name for username or password.")
    # Raising the UnboundLocalError exception if one or more variables don't exist due to invalid data being sent to the database, printing an error message and the traceback
    except UnboundLocalError:
        traceback.print_exc()
        print("Data Error. Referencing variables that are not declared. User sent a username or password without content.")
    # Raising the TypeError exception if the user sends data with inappropriate data types, printing an error message and the traceback
    except TypeError:
        traceback.print_exc()
        print("Data Error. Invalid data type for username or password.")
    # Raising the ValueError exception if the user sends data with appropriate data types but invalid values, printing an error message and the traceback
    except ValueError:
        traceback.print_exc()
        print("Invalid data was sent to the database.")
    # Raising a general exception to catch all other errors, printing a general error message and the traceback
    except:
        traceback.print_exc()
        print("An error has occured.")
        # Sending the user a client error response and stopping the function from running the next lines of code that interacts with the database
        return Response("Data Error. Invalid data was sent to the database.", mimetype="text/plain", status=400)

    # Opening the database and creating a cursor
    conn = dbconnect.open_db_connection()
    cursor = dbconnect.create_db_cursor(conn)

    # Checking to see if the database connection is opened and whether the cursor is created
    check_db_connection_and_cursor(conn, cursor)

    # Assigning the new id of the user to be a negative number to indicate that a new id was not created
    new_user_id = -1

    # Creating a try-except block to catch errors when storing the new user into the database
    try:
        # Storing the user's username and password into the database and commiting the changes
        cursor.execute("INSERT INTO users(username, password) VALUES(?, ?)", [username, password])
        conn.commit()
        # Getting the new id of the new user created
        new_user_id = cursor.lastrowid
    # Raising the UnboundLocalError exception if one or more variables don't exist due to invalid data being sent to the database, printing an error message and the traceback
    except UnboundLocalError:
        traceback.print_exc()
        print("Data Error. Referencing variables that are not declared. User sent a username or password without content.")
    # Raising the DataError exception if the database is unable to process the data, printing an error message and the traceback
    except mariadb.DataError:
        traceback.print_exc()
        print("Data Error. Invalid data was sent to the database.")
    # Raising an IntegrityError exception if the username that already exists in the database, printing an error message and the traceback
    except mariadb.IntegrityError:
        traceback.print_exc()
        print(f"Unique key constraint failure. {username} already exists in the database.")
    # Raising the OperationalError exception for things that are not in control of the programmer, printing an error message and the traceback
    except mariadb.OperationalError:
        traceback.print_exc()
        print("An operational error has occured when creating the user.")
    # Raising the ProgrammingError exception for errors made by the programmer, printing an error message and the traceback
    except mariadb.ProgrammingError:
        traceback.print_exc()
        print("Invalid SQL syntax.")
    # Raising the DatabaseError exception for errors related to the database, printing an error message and the traceback
    except mariadb.DatabaseError:
        traceback.print_exc()
        print("An error in the database has occured. Failed to create user.")
    # Raising a general exception to catch all other errors, printing a general error message and the traceback
    except:
        traceback.print_exc()
        print("An error has occured.")

    # Closing the cursor and database connection
    close_db_connection_and_cursor(conn, cursor)

    # If the new id was not created, send the user a client error response
    if(new_user_id == -1):
        return Response("Failed to sign up.", mimetype="text/plain", status=500)
    # If the new id was created, send the user their credentials in JSON format and a client success response
    else:
        new_signup = {
            'id': new_user_id,
            'username': username,
        }
        new_signup_json = json.dumps(new_signup, default=str)
        return Response(new_signup_json, mimetype="application/json", status=201)

# Created a POST request to the "login" endpoint to log in users into their exisiting account
@app.post("/login")
def login_user():
    # Using a try-except block to catch errors when the user logs in
    try:
        # Receiving the user's username and password and storing it as a variable
        username = request.json['username']
        password = request.json['password']

        # If the username or password is not provided by the user, send a client error response
        if(username == None or username == "" or password == None or password == ""):
            return Response("Username and password do not match the database records.", mimetype="text/plain", status=400)
    # Raising the KeyError exception if the user sends data with the incorrect key names, printing an error message and the traceback
    except KeyError:
        traceback.print_exc()
        print("Key Error. Incorrect Key name for the username or password.")
    # Raising the UnboundLocalError exception if one or more variables don't exist due to invalid data being sent to the database, printing an error message and the traceback
    except UnboundLocalError:
        traceback.print_exc()
        print("Data Error. Referencing variables that are not declared.")
    # Raising the TypeError exception if the user sends data with inappropriate data types, printing an error message and the traceback
    except TypeError:
        traceback.print_exc()
        print("Data Error. Invalid data type for username or password.")
    # Raising the ValueError exception if the user sends data with appropriate data types but invalid values, printing an error message and the traceback
    except ValueError:
        traceback.print_exc()
        print("Invalid data was sent to the database.")
    # Raising a general exception to catch all other errors, printing a general error message and the traceback
    except:
        traceback.print_exc()
        print("An error has occured.")
        # Sending the user a client error response and stopping the function from running the next lines of code that interacts with the database
        return Response("Username and password do not match the database records.", mimetype="text/plain", status=400)
    
    # Opening the database and creating a cursor
    conn = dbconnect.open_db_connection()
    cursor = dbconnect.create_db_cursor(conn)

    # Checking to see if the database connection is opened and whether the cursor is created
    check_db_connection_and_cursor(conn, cursor)

    # Initializing the variables so that it can still be used after the try-except block
    database_login_info = None
    row_count = 0

    # Creating a try-except block to catch errors when checking the user's login credentials
    try:
        # Getting the username, password and id of the user and getting the number of rows that are selected with the given username and password
        cursor.execute("SELECT username, password, id FROM users WHERE username = ? AND password = ?", [username, password])
        database_login_info = cursor.fetchall()
        row_count = cursor.rowcount
    # Raising the UnboundLocalError exception if one or more variables don't exist due to invalid data being sent to the database, printing an error message and the traceback
    except UnboundLocalError:
        traceback.print_exc()
        print("Data Error. Referencing variables that are not declared.")
    # Raising the DataError exception if the database is unable to process the data, printing an error message and the traceback
    except mariadb.DataError:
        traceback.print_exc()
        print("Data Error. Invalid data was sent to the database.")
    # Raising an IntegrityError exception if the username that already exists in the database, printing an error message and the traceback
    except mariadb.IntegrityError:
        traceback.print_exc()
        print(f"Unique key constraint failure. {username} already exists in the database.")
    # Raising the OperationalError exception for things that are not in control of the programmer, printing an error message and the traceback
    except mariadb.OperationalError:
        traceback.print_exc()
        print("An operational error has occured when verifying the user's credentials.")
    # Raising the ProgrammingError exception for errors made by the programmer, printing an error message and the traceback
    except mariadb.ProgrammingError:
        traceback.print_exc()
        print("Invalid SQL syntax.")
    # Raising the DatabaseError exception for errors related to the database, printing an error message and the traceback
    except mariadb.DatabaseError:
        traceback.print_exc()
        print("An error in the database has occured. Unable to verify the user's credentials.")
    # Raising a general exception to catch all other errors, printing a general error message and the traceback
    except:
        traceback.print_exc()
        print("An error has occured.")

    # Closing the cursor and database connection
    close_db_connection_and_cursor(conn, cursor)

    # If the username and password matches with the username and password stored in the database, send the user their login credentials and a client success response
    if(row_count == 1):
        user_login = {
            'id': database_login_info[0][2],
            'username': username,
        }
        user_login_json = json.dumps(user_login, default=str)
        return Response(user_login_json, mimetype="application/json", status=200)
    # If the username and password do not match, send a client error response
    else:
        return Response("Failed to log in.", mimetype="text/plain", status=500)

# Creating a GET request to the "candy" endpoint to get all candies
@app.get("/candy")
def get_candy_list():
    # Opening the database and creating a cursor
    conn = dbconnect.open_db_connection()
    cursor = dbconnect.create_db_cursor(conn)

    # Checking to see if the database connection is opened and whether the cursor is created
    check_db_connection_and_cursor(conn, cursor)

    # Initializing the candy list and assigning it a value so that it can still be referenced after the try-except block
    candy_list = None

    # Creating a try-except block to catch errors when getting all candies from the database
    try:
        # Getting the all candies from the database
        cursor.execute("SELECT name, description, price_in_dollars, image_url, user_id, id FROM candy")
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
        user_id = int(request.json.get('userId'))

        # If the candy name or price is not provided by the user, send a client error response
        if(candy_name == None or candy_name == "" or candy_price == None or candy_price == "" or user_id == None or user_id == ""):
            return Response("Invalid data was sent to the database. Failed to create candy.", mimetype="text/plain", status=400)
        
        # If the user chooses to create a candy post without adding content to the description, set the description as an empty string
        if(candy_description == None or candy_description == ""):
            candy_description = ""
        
        # If the user chooses to create a candy post without adding a image URL, set the image URL as an empty string
        if(candy_image == None or candy_image == ""):
            candy_image = ""
    # Raising the KeyError exception if the user sends data with the incorrect key names, printing an error message and the traceback
    except KeyError:
        traceback.print_exc()
        print("Key Error. Incorrect Key name of data.")
    # Raising the UnboundLocalError exception if one or more variables don't exist due to invalid data being sent to the database, printing an error message and the traceback
    except UnboundLocalError:
        traceback.print_exc()
        print("Data Error. Referencing variables that are not declared.")
    # Raising the TypeError exception if the user sends data with inappropriate data types, printing an error message and the traceback
    except TypeError:
        traceback.print_exc()
        print("Data Error. Invalid data type sent to the database.")
    # Raising the ValueError exception if the user sends data with appropriate data types but invalid values, printing an error message and the traceback
    except ValueError:
        traceback.print_exc()
        print("Invalid data was sent to the database.")
    # Raising a general exception to catch all other errors, printing a general error message and the traceback
    except:
        traceback.print_exc()
        print("An error has occured.")
        # Sending the user a client error response and stopping the function from running the next lines of code that interacts with the database
        return Response("Invalid data was sent to the database. Failed to create candy.", mimetype="text/plain", status=400)

    # If the user sends valid data, open the database connection and create a cursor
    conn = dbconnect.open_db_connection()
    cursor = dbconnect.create_db_cursor(conn)

    # Checking to see if the database connection is opened and whether the cursor is created
    check_db_connection_and_cursor(conn, cursor)

    # Assign the new id of the candy to be a negative number which indicates that a new id was not created
    new_candy_id = -1

    # Creating a try-except block to catch errors when inserting the new candy into the database
    try:
        # Inserting the new candy into the database and commiting the changes
        cursor.execute("INSERT INTO candy(name, description, price_in_dollars, image_url, user_id) VALUES(?, ?, ?, ?, ?)", [candy_name, candy_description, candy_price, candy_image, user_id])
        conn.commit()
        # Getting the id of the new candy
        new_candy_id = cursor.lastrowid
    # Raising an IndexError exception if the user enters an id that does not exist in the database, printing an error message and the traceback
    except IndexError:
        traceback.print_exc()
        print(f"User with an id of {user_id} does not exist in the database.")
    # Raising the UnboundLocalError exception if one or more variables don't exist due to invalid data being sent to the database, printing an error message and the traceback
    except UnboundLocalError:
        traceback.print_exc()
        print("Data Error. Referencing variables that are not declared.")
    # Raising an IntegrityError exception if the user sends data that conflicts with the key contraints, printing an error message and the traceback
    except mariadb.IntegrityError:
        traceback.print_exc()
        print("Unique key constraint failure. Candy name and description must be unique.")
    # Raising the DataError exception if the database is unable to process the data, printing an error message and the traceback
    except mariadb.DataError:
        traceback.print_exc()
        print("Data Error. Invalid data was sent to the database.")
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
    if(new_candy_id == -1):
        return Response("Failed to create a new candy.", mimetype="text/plain", status=500)
    # If the new id was created, send the user the new candy in JSON format and a client success response
    else:
        new_candy_json = json.dumps([candy_name, candy_description, candy_price, candy_image, user_id, new_candy_id], default=str)
        return Response(new_candy_json, mimetype="application/json", status=201)

# Creating a DELETE request to the "candy" endpoint to delete an exisiting candy
@app.delete("/candy")
def delete_candy():
    # Creating a try-except block to catch errors when receiving the candy and user id sent by the user
    try:
        # Converting both ids into an integer data type
        candy_id = int(request.json['candyId'])
        user_id = int(request.json['userId'])
    # Raising the KeyError exception if the user sends data with the incorrect key names
    except KeyError:
        traceback.print_exc()
        print("Key Error. Incorrect Key name of data.")
    # Raising an IndexError exception if the user enters an id that does not exist in the database
    except IndexError:
        traceback.print_exc()
        print("The candy id or user id does not exist in the database.")
    # Raising the TypeError exception if the user sends an id that has a data type other than an integer, printing an error message and the traceback
    except TypeError:
        traceback.print_exc()
        print("Data Error. Invalid data type sent to the database.")
    # Raising the ValueError exception if the user sends data with appropriate data types but invalid values
    except ValueError:
        traceback.print_exc()
        print("Invalid data was sent to the database.")
    # Raising a general exception to catch all other errors, printing a general error message and the traceback
    except:
        traceback.print_exc()
        print("An error has occured.")
        # Sending the user a client error response and stopping the function for running the next lines of code that interacts with the database
        return Response("Invalid data was sent to the database. Failed to delete candy.", mimetype="text/plain", status=400)

    # If the user sends a valid id, open the database connection and create a cursor
    conn = dbconnect.open_db_connection()
    cursor = dbconnect.create_db_cursor(conn)

    # Checking to see if the database connection is opened and whether the cursor is created
    check_db_connection_and_cursor(conn, cursor)

    # Initializing the row count and assigning it a value so that it can still be referenced after the try-except block
    row_count = 0

    # Creating a try-except block to catch errors when deleting a candy from the database
    try:
        # Deleting a candy from the database and committing the changes
        cursor.execute("DELETE FROM candy WHERE user_id = ? AND id = ? ", [user_id, candy_id])
        conn.commit()
        # Getting the number of rows that have been deleted from the database
        row_count = cursor.rowcount
    # Raising the OperationalError exception for things that are not in control of the programmer, printing an error message and the traceback
    except mariadb.OperationalError:
        traceback.print_exc()
        print(f"An operational error has occured. Failed to delete candy with an id of {candy_id} in the database.")
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

    # Checking to see if the database connection is opened and whether the cursor is created
    check_db_connection_and_cursor(conn, cursor)

    # Initalizing the unedited candy as a variable and assigning it a value so that it can still be referenced after the try-except block
    old_candy = None
    
    # Creating a try-except block to catch errors when getting all the old candies from the database
    try:
        # Converting the candy and user id into an integer and getting the unedited candy from the database
        candy_id = int(request.json['candyId'])
        user_id = int(request.json['userId'])
        cursor.execute("SELECT name, description, price_in_dollars, image_url, user_id, id FROM candy WHERE user_id = ? AND id = ?", [user_id, candy_id])
        old_candy = cursor.fetchall()
    # Raising the KeyError exception if the user sends data with the incorrect key names
    except KeyError:
        traceback.print_exc()
        print("Key Error. Incorrect Key name for the user id or candy id.")
    # Raising an IndexError exception if the user enters an id that does not exist in the database
    except IndexError:
        traceback.print_exc()
        print(f"The candy id of {candy_id} or user id of {user_id} does not exist in the database.")
    # Raising the TypeError exception if the user sends an id that has a data type other than an integer, printing an error message and the traceback
    except TypeError:
        traceback.print_exc()
        print("Data Error. Invalid data type sent to the database.")
    # Raising the ValueError exception if the user sends data with appropriate data types but invalid values
    except ValueError:
        traceback.print_exc()
        print("Invalid data was sent to the database.")
    # Raising a general exception to catch all other errors, printing a general error message and the traceback
    except:
        print("An error has occured.")
        traceback.print_exc()
        # If the database failed to delete the candy, send a client error response
        return Response("Invalid data was sent to the database. Failed to edit candy.", mimetype="text/plain", status=400)

    # Closing the cursor and database connection
    close_db_connection_and_cursor(conn, cursor)

    # If the candy id was invalid or the list of old candies could not be retrieved from the database, send a client server error
    if(candy_id == None or user_id == None or old_candy == None):
        return Response("Invalid data being passed to the database. Failed to edit candy.", mimetype="text/plain", status=400)

    # Creating a try-except block to catch errors when updating a candy
    try:
        # Receiving the user's data
        candy_name = request.json.get('name')
        candy_description = request.json.get('description')
        candy_price = request.json.get('priceInDollars')
        candy_image = request.json.get('imageUrl')

        # If the database contains the old candy name with valid content but the user updates the candy name without content, set the current name to the old candy name
        if((old_candy[0][0] != None or old_candy[0][0] != "") and (candy_name == None or candy_name == "")):
            candy_name = old_candy[0][0]

        # If the database contains the old candy description with valid content but the user updates the description without content, set the current description to the old candy description
        if((old_candy[0][1] != None or old_candy[0][1] != "") and (candy_description == None or candy_description == "")):
            candy_description = old_candy[0][1]
        # If the database contains the old candy description which initially had no content and the user has not updated the description with content, set the current description as an empty string
        elif((old_candy[0][1] == None or old_candy[0][1] == "") and (candy_description == None or candy_description == "")):
            candy_description == ""

        # If the database contains the old candy price with valid content but the user updates the price without content, set the current price to the old candy price
        if((old_candy[0][2] != None or old_candy[0][2] != "") and (candy_price == None or candy_price == "")):
            candy_price = old_candy[0][2]
        
        # If the database contains the old candy image with valid content but the user updates the image without content, set the current image to the old candy image
        if((old_candy[0][3] != None or old_candy[0][3] != "") and (candy_image == None or candy_image == "")):
            candy_image = old_candy[0][3]
        # If the database contains the old candy image url which initially had no content and the user has not updated the image url with content, set the current image url as an empty string
        elif((old_candy[0][3] == None or old_candy[0][3] == "") and (candy_image == None or candy_image == "")):
            candy_image == ""
    # Raising the KeyError exception if the user sends data with the incorrect key names, printing an error message and the traceback
    except KeyError:
        traceback.print_exc()
        print("Key Error. Incorrect Key names.")
    # Raising the UnboundLocalError exception if one or more variables don't exist due to invalid data being sent to the database
    except UnboundLocalError:
        traceback.print_exc()
        print("Data Error. Referencing variables that are not declared.")
    # Raising the TypeError exception if the user sends data with inappropriate data types, printing an error message and the traceback
    except TypeError:
        traceback.print_exc()
        print("Data Error. Invalid data type sent to the database.")
    # Raising the ValueError exception if the user sends data with appropriate data types but invalid values
    except ValueError:
        traceback.print_exc()
        print("Invalid data was sent to the database.")
    # Raising a general exception to catch all other errors, printing a general error message and the traceback
    except:
        traceback.print_exc()
        print("An error has occured.")
        # Sending the user a client error response and stopping the function from running the next lines of code that interacts with the database
        return Response("Invalid data was sent to the database. Failed to edit candy.", mimetype="text/plain", status=400)
    
    # If the user sends valid data, open the database connection and create a cursor 
    conn = dbconnect.open_db_connection()
    cursor = dbconnect.create_db_cursor(conn)

    # Checking to see if the database connection is opened and whether the cursor is created
    check_db_connection_and_cursor(conn, cursor)

    # Initializing the row count and assigning it a value so that it can still be referenced after the try-except block
    row_count = 0

    # Creating a try-except block to catch errors when updating the candy to the database
    try:
        # Replacing the edited candy with the old candy and commiting the changes
        cursor.execute("UPDATE candy SET name = ?, description = ?, price_in_dollars = ?, image_url = ? WHERE user_id = ? AND id = ?", [candy_name, candy_description, candy_price, candy_image, user_id, candy_id])
        conn.commit()
        # Getting the number of rows that have been updated in the database
        row_count = cursor.rowcount
    # Raising an IntegrityError exception if the user sends data that conflicts with the key contraints, printing an error message and the traceback
    except mariadb.IntegrityError:
        traceback.print_exc()
        print("Unique key constraint failure. Candy name and description must be unique.")
    # Raising the DataError exception if the database is unable to process the data, printing an error message and the traceback
    except mariadb.DataError:
        traceback.print_exc()
        print("Data Error. Invalid data was sent to the database.")
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
        edited_candy_json = json.dumps([candy_name, candy_description, candy_price, candy_image, user_id, candy_id], default=str)
        return Response(edited_candy_json, mimetype="application/json", status=200)
    # If the user did not modify their candy post, send the user back the old candy data
    elif(row_count == 0):
        old_candy_json = json.dumps(old_candy[0], default=str)
        return Response(old_candy_json, mimetype="application/json", status=200)
    # If the database failed to store the edited candy, send the user a server error response
    else:
        return Response("Failed to edit candy.", mimetype="text/plain", status=500)

# Running the flask server with debug mode turned on
app.run(debug=True)