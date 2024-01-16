from flask import Flask, render_template, request, jsonify
import pymongo
import mysql.connector
import psycopg2
import math
import cx_Oracle

app = Flask(__name__)

# dictionary containe all location of site that we have
database_locations = {
    'mongo_db1': {'latitude': 35.74139, 'longitude': -5.8374}, # TANGER ahlan
    'mongo_db2': {'latitude': 30.40696, 'longitude': -9.57708},   # AGADIR sidi youssef
    'mysql_db1':{'latitude': 34.226017, 'longitude': -5.712916},    # SIDI KACEM
    'mysql_db2':{'latitude': 27.15003, 'longitude': -13.19388},  # LAAYOUNE
    'postgres_db': {'latitude': 33.99969, 'longitude': -6.85292}, # RABAT agdal
    'oracle_db1': {'latitude': 34.25761, 'longitude': -6.58302}, #KENITRA  maamoura
    'oracle_db2': {'latitude': 33.8961, 'longitude': -6.58807} # MEKNAS salam II
}

def get_closest_database(lat, long):
    closest_db = None
    min_distance = float('inf')
    for db, db_location in database_locations.items():
        distance = haversine(lat, long, db_location['latitude'], db_location['longitude'])
        if distance < min_distance:
            min_distance = distance
            closest_db = db
    print("You are connected to ==> ",closest_db)

    return closest_db

def haversine(lat1, lon1, lat2, lon2):
    # Haversine formula to calculate distance between two points on the Earth
    R = 6371  # Radius of the Earth in kilometers

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (math.sin(math.radians(dlat) / 2) ** 2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * (math.sin(math.radians(dlon) / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    print("Distance =",distance)
    return distance

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/query', methods=['POST'])

def execute_query():
    query = request.form.get('query')
    lat = float(request.form.get('lat'))
    long = float(request.form.get('long'))

    # Determine the closest database based on user's location
    closest_db_key = get_closest_database(lat, long)

    # Attempt to connect to the closest database
    closest_db = connect_to_database(closest_db_key)

    # If the connection to the closest database fails, try the next closest database
    if closest_db is None:
        next_closest_db_key = get_next_closest_database(lat, long, excluded_db_key=closest_db_key)
        closest_db = connect_to_database(next_closest_db_key)

    # Execute the query on the selected database
    result = execute_query_on_database(query, closest_db)

    # Trigger the action after query execution
    query_execution_trigger(query, lat, long)

    return jsonify({'result': result})
def query_execution_trigger(query, lat, long):
    # Send a notification
    send_notification("Query executed", f"User executed query: {query} at location: ({lat}, {long})")

def send_notification(subject, message):
    # In this example, print the notification message
    print(f"Notification: {subject} - {message}")

def get_next_closest_database(lat, long, excluded_db_key):
    # Get the next closest database excluding the one that failed
    # Implement a similar logic as get_closest_database but skip the excluded database
    next_closest_db = None
    min_distance = float('inf')

    for db, db_location in database_locations.items():
        if db != excluded_db_key:
            distance = haversine(lat, long, db_location['latitude'], db_location['longitude'])
            if distance < min_distance:
                min_distance = distance
                next_closest_db = db

    return next_closest_db



def connect_to_database(db_key):
    if db_key == 'mongo_db1':
        # Replace with actual MongoDB connection details
        return pymongo.MongoClient("mongodb://aimanoth54:@lolaimanothAIMAN@mongo_db1_host:27017")['database1']
    elif db_key == 'mongo_db2':
        # Replace with actual MongoDB connection details
        return pymongo.MongoClient("mongodb://ayoubzarou4:ayoub4637#77@mongo_db2_host:27018")['database2']
    elif db_key == 'mysql_db1':
        # Replace with actual MySQL connection details
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="db1"
        )
    elif db_key == 'mysql_db2':
        # Replace with actual MySQL connection details
        return mysql.connector.connect(
            host="https://8ce0-160-179-161-252.ngrok-free.app",
            user="root",
            password="hmza2023",
            database="db1"
        )
    elif db_key == 'postgres_db':
        # Replace with actual PostgreSQL connection details
        return psycopg2.connect(
            host="@ec2-52-7-132-25.compute-1.amazonaws.com",
            user="ompnmmrvahagdt",
            password="28443eb41bc9abd01d9e8e0ce0243b6a17b4c3d22e47bf79da17526d00e16dc6",
            database="db1"
        )
    elif db_key == 'oracle_db1':
        # Replace with actual Oracle connection details
        connection = cx_Oracle.connect(
            user="aimanmhr",
            password="ENSEM@casa2023",
            dsn="8.8.8.8"
        )
        return connection
    elif db_key == 'oracle_db2':
        # Replace with actual Oracle connection details
        connection = cx_Oracle.connect(
            user="hamza352",
            password="test253hamza@",
            dsn="8.8.8.8"
        )
        return connection
        

def execute_query_on_database(query, db_connection):
    # Implement logic to execute the query on the specified database
    # Return the query result
    if isinstance(db_connection, pymongo.database.Database):
        return db_connection.command('aggregate', 'collection1', pipeline=[{'$match': {'field': 'value'}}])
    elif isinstance(db_connection, mysql.connector.connection.MySQLConnection):
        cursor = db_connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    elif isinstance(db_connection, psycopg2.extensions.connection):
        cursor = db_connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    # Add more database-specific query execution logic...

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
