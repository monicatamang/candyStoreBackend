import dbcreds
import mariadb
import traceback

# Creating a function that opens that database connection
def open_db_connection():
    # Using a try-except block to catch errors when connecting to the database
    try:
        # Trying to return the connection object to the caller
        return mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
    # Raising the OperationalError exception for things that are not in control of the programmer, printing an error message and the traceback
    except mariadb.OperationalError:
        print("Operational errors detected in the database connection.")
        traceback.print_exc()
    # Raising the DatabaseError exception for errors related to the database, printing an error message and the traceback
    except mariadb.DatabaseError:
        # A DatabaseError exception is raised for all errors that are related to the database
        print("Error detected in the database and resulted in a connection failure.")
        traceback.print_exc()
    # Raising a general exception to catch all other errors, printing a general error message and the traceback
    except:
        print("An error has occured. Failed to connect to the database.")
        traceback.print_exc()

# Creating a function that returns a cursor object using the current connection, which is passed as an argument
def create_db_cursor(conn):
    # Using a try-except block to catch errors when creating a cursor
    try:
        # Trying to return a cursor object using the current connection
        return conn.cursor()
    # Raising an InternalError exception if the cursor is invalid
    except mariadb.InternalError:
        print("Internal errors detected in the database. Failed to create a cursor.")
        traceback.print_exc()
    # Raising the OperationalError exception for things that are not in control of the programmer, printing an error message and the traceback
    except mariadb.OperationalError:
        print("Operational errors detected in the database connection. Failed to create a cursor.")
        traceback.print_exc()
    # Raising the DatabaseError exception for errors related to the database, printing an error message and the traceback
    except mariadb.DatabaseError:
        print("Errors detected in database. Failed to create a cursor.")
        traceback.print_exc()
    # Raising a general exception to catch all other errors, printing a general error message and the traceback
    except:
        print("An error has occured. Failed to create a cursor.")
        traceback.print_exc()

# Creating a function that closes the cursor
def close_cursor(cursor):
    # Checking to see if the cursor was initially created and if it wasn't, don't attempt to close the cursor
    if(cursor == None):
        return True
    # Using a try-except block to catch errors when closing the cursor
    try:
        # Trying to close the cursor, returning "True" to indicate that the cursor was closed successfully
        cursor.close()
        return True
    # Raising an InternalError exception if the cursor is invalid
    except mariadb.InternalError:
        print("Internal errors detected in the database. Failed to create a cursor.")
        traceback.print_exc()
    # Raising the OperationalError exception for things that are not in control of the programmer, printing an error message and the traceback
    except mariadb.OperationalError:
        print("Operational errors detected in the database connection. Failed to create a cursor.")
        traceback.print_exc()
    # Raising the DatabaseError exception for errors related to the database, printing an error message and the traceback
    except mariadb.DatabaseError:
        # A DatabaseError exception is raised for all errors that are related to the database
        print("Errors detected with the current connection. Failed to close cursor.")
        traceback.print_exc()
    # Raising a general exception to catch all other errors, printing a general error message and the traceback
    except:
        print("An error has occured. Failed to close cursor.")
        traceback.print_exc()
        return False

# Creating a function that closes the database connection
def close_db_connection(conn):
    # If the database connect was not initially opened, don't attempt to close it
    if(conn == None):
        return True
    # Using a try-except block to catch errors when closing the database connection
    try:
        # Trying to close the connection, returning "True" to indicate that the connection was close successfully
        conn.close()
        return True
    # Raising the OperationalError exception for things that are not in control of the programmer, printing an error message and the traceback
    except mariadb.OperationalError:
        print("Optional errors detected in the database. Failed to close the connection.")
        traceback.print_exc()
    # Raising the DatabaseError exception for errors related to the database, printing an error message and the traceback
    except mariadb.DatabaseError:
        print("Errored detected in the database. Failed to close the connection.")
        traceback.print_exc()
    # Raising a general exception to catch all other errors, printing a general error message and the traceback
    except:
        print("An error has occured. Failed to close database connection.")
        traceback.print_exc()
        return False