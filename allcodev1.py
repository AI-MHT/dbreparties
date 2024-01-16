from flask import Flask, render_template, request, jsonify
from geopy.geocoders import Nominatim
import pymongo
import mysql.connector
import psycopg2
import math

app = Flask(__name__)

# Create a dictionary to map each database to its location
database_locations = {
    'mongo_db1': {'latitude': 41.8781, 'longitude': -87.6298}, # Replace with actual coordinates
    'mongo_db2': {'latitude': 37.7749, 'longitude': -122.4194},   # Replace with actual coordinates
    'mysql_db1':{'latitude': 40.7128, 'longitude': -74.0060},    # Replace with actual coordinates
    'mysql_db2':{'latitude': 34.0522, 'longitude': -118.2437},  # Replace with actual coordinates
    'postgres_db': {'latitude': 39.9526, 'longitude': -75.1652}  # Replace with actual coordinates
    # Add more databases as needed...
}

def get_closest_database(lat, long):
    # Implement logic to determine the closest database based on lat and long
    closest_db = None
    min_distance = float('inf')

    for db, db_location in database_locations.items():
        distance = haversine(lat, long, db_location['latitude'], db_location['longitude'])
        if distance < min_distance:
            min_distance = distance
            closest_db = db
    print("HHHHHHHHHHH",closest_db)

    return closest_db

def haversine(lat1, lon1, lat2, lon2):
    # Haversine formula to calculate distance between two points on the Earth
    R = 6371  # Radius of the Earth in kilometers

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (math.sin(math.radians(dlat) / 2) ** 2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * (math.sin(math.radians(dlon) / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    print(distance)
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

    # Connect to the closest database
    closest_db = connect_to_database(closest_db_key)

    # Execute the query on the selected database
    result = execute_query_on_database(query, closest_db)

    return jsonify({'result': result})

def connect_to_database(db_key):
    # Implement logic to connect to the specified database
    # Return the database connection object
    if db_key == 'mongo_db1':
        return pymongo.MongoClient("mongodb://localhost:27017")['database1']
    elif db_key == 'mongo_db2':
        return pymongo.MongoClient("mongodb://localhost:27018")['database2']
    elif db_key == 'mysql_db1':
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="db1"
        )
    elif db_key == 'mysql_db2':
        return mysql.connector.connect(
            host="localhost",
            user="user",
            password="password",
            database="database2"
        )
    elif db_key == 'postgres_db':
        return psycopg2.connect(
            host="localhost",
            user="user",
            password="password",
            database="database"
        )
    # Add more database connections as needed...

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
