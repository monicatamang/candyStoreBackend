from flask import Flask, request, Response
import dbhelpers
import json
import traceback

# Creating a function to create a candy post
def create_candy():
    # Trying to get the user's data
    try:
        login_token = request.json['loginToken']
        candy_name = request.json.get('name')
        candy_description = request.json.get('description')
        candy_price = float(request.json.get('priceInDollars'))
        candy_image = request.json.get('imageUrl')

        # If the candy name or price is not provided by the user, send a client error response
        if(candy_name == None or candy_name == "" or candy_price == None or candy_price == "" or login_token == None or login_token == ""):
            return Response("Invalid data was sent to the database. Failed to create candy.", mimetype="text/plain", status=400)
        
        # If the user chooses to create a candy post without adding content to the description, set the description as an empty string
        if(candy_description == None or candy_description == ""):
            candy_description = ""
        
        # If the user chooses to create a candy post without adding a image URL, set the image URL as an empty string
        if(candy_image == None or candy_image == ""):
            candy_image = ""
    except KeyError:
        traceback.print_exc()
        print("Key Error. Incorrect Key name of data.")
        return Response("Invalid data was sent to the database. Failed to create candy.", mimetype="text/plain", status=400)
    except TypeError:
        traceback.print_exc()
        print("Data Error. Invalid data type sent to the database.")
        return Response("Invalid data was sent to the database. Failed to create candy.", mimetype="text/plain", status=400)
    except ValueError:
        traceback.print_exc()
        print("Invalid data was sent to the database.")
        return Response("Invalid data was sent to the database. Failed to create candy.", mimetype="text/plain", status=400)
    except:
        traceback.print_exc()
        print("An error has occured.")
        return Response("Invalid data was sent to the database. Failed to create candy.", mimetype="text/plain", status=400)

    # Trying to get the user's id given their login token
    user_id = dbhelpers.run_select_statement("SELECT user_id FROM user_session WHERE token = ?", [login_token,])

    # If the user's id is retrieved from the database, try to insert the user's data into the database
    if(len(user_id) == 1):
        new_candy_id = dbhelpers.run_insert_statement("INSERT INTO candy(name, description, price_in_dollars, image_url, user_id) VALUES(?, ?, ?, ?, ?)", [candy_name, candy_description, candy_price, candy_image, user_id[0][0]])

        # If the user's data was not inserted into the database, send a server error response
        if(new_candy_id == None):
            return Response("Failed to create a candy post.", mimetype="text/plain", status=500)
        # If the user's data was inserted into the database, try to get the new candy post from the database
        else:
            new_candy = dbhelpers.run_select_statement("SELECT c.name, c.description, c.price_in_dollars, c.image_url, c.user_id, c.id, u.username FROM users u INNER JOIN candy c ON c.user_id = u.id WHERE u.id = ? AND c.id = ?", [user_id[0][0], new_candy_id])

            # If the new candy post is retrieved from the database, send a client success response with the candy post as JSON
            if(len(new_candy) == 1):
                new_candy_json = json.dumps(new_candy[0], default=str)
                return Response(new_candy_json, mimetype="application/json", status=201)
            # If the new candy post is not retrieved from the database, send a server error response
            else:
                return Response("Failed to create a new candy.", mimetype="text/plain", status=500)
    # If the user's id is not retrieved from the database, send a client error response
    else:
        return Response("User is not logged in.", mimetype="text/plain", status=400)