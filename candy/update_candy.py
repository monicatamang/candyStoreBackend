from flask import Flask, request, Response
import dbhelpers
import json
import traceback

# Creating a function that edits a candy post
def edit_candy():
    # Trying to get the user's login token and candy id
    try:
        login_token = request.json['loginToken']
        candy_id = int(request.json['candyId'])
    except KeyError:
        traceback.print_exc()
        print("Key Error. Incorrect Key name for the user id or candy id.")
        return Response("Invalid data was sent to the database. Failed to edit candy.", mimetype="text/plain", status=400)
    except:
        traceback.print_exc()
        print("An error has occured.")
        return Response("Invalid data was sent to the database. Failed to create candy.", mimetype="text/plain", status=400)

    # Trying to get the user's id from the database given the login token
    user_id = dbhelpers.run_select_statement("SELECT user_id FROM user_session WHERE token = ?", [login_token,])

    # If the user is logged in, get the original candy post from the database
    if(len(user_id) == 1):
        old_candy = dbhelpers.run_select_statement("SELECT c.name, c.description, c.price_in_dollars, c.image_url, c.user_id, c.id, u.username FROM users u INNER JOIN candy c ON u.id = c.user_id WHERE u.id = ? AND c.id = ?", [user_id[0][0], candy_id])

        # If the candy id was invalid or the list of old candies could not be retrieved from the database, send a client server error
        if(old_candy == None):
            return Response("Invalid data being passed to the database. Failed to edit candy.", mimetype="text/plain", status=400)

        # Trying to get the user's data
        try:
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
        except KeyError:
            traceback.print_exc()
            print("Key Error. Incorrect Key names.")
            return Response("Invalid data was sent to the database. Failed to edit candy.", mimetype="text/plain", status=400)
        except IndexError:
            traceback.print_exc()
            print("The candy id or user id does not exist in the database.")
            return Response("Invalid data was sent to the database. Failed to edit candy.", mimetype="text/plain", status=400)
        except UnboundLocalError:
            traceback.print_exc()
            print("Data Error. Referencing variables that are not declared.")
            return Response("Invalid data was sent to the database. Failed to edit candy.", mimetype="text/plain", status=400)
        except TypeError:
            traceback.print_exc()
            print("Data Error. Invalid data type sent to the database.")
            return Response("Invalid data was sent to the database. Failed to edit candy.", mimetype="text/plain", status=400)
        except ValueError:
            traceback.print_exc()
            print("Invalid data was sent to the database.")
            return Response("Invalid data was sent to the database. Failed to edit candy.", mimetype="text/plain", status=400)
        except:
            traceback.print_exc()
            print("An error has occured.")
            return Response("Invalid data was sent to the database. Failed to edit candy.", mimetype="text/plain", status=400)

        # Trying to update the user's candy post
        row_count = dbhelpers.run_update_statement("UPDATE candy SET name = ?, description = ?, price_in_dollars = ?, image_url = ? WHERE user_id = ? AND id = ?", [candy_name, candy_description, candy_price, candy_image, user_id[0][0], candy_id])

        # If the user's candy post is updated, get the updated candy post from the database
        if(row_count == 1):
            edited_candy = dbhelpers.run_select_statement("SELECT c.name, c.description, c.price_in_dollars, c.image_url, c.user_id, c.id, u.username FROM users u INNER JOIN candy c WHERE u.id = ? AND c.id = ?", [user_id[0][0], candy_id])
            # If the updated candy post is retrieved from the database, send a client success response with the updated candy post as JSON
            if(len(edited_candy) == 1):
                edited_candy_json = json.dumps(edited_candy[0], default=str)
                return Response(edited_candy_json, mimetype="application/json", status=200)
            # If the updated candy post is not retrieved from the database, send a server error response
            else:
                return Response("Failed to edit candy.", mimetype="text/plain", status=500)
        # If the user's candy post is not updated, send a server error response
        else:
            return Response("Failed to edit candy.", mimetype="text/plain", status=500)
    # If the user is not logged in, send a client error response
    else:
        return Response("User is not logged in.", mimetype="text/plain", status=400) 