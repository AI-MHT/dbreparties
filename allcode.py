from flask import Flask, render_template, request, jsonify
from geopy.geocoders import Nominatim
import pymongo
import mysql.connector
import psycopg2
import math

app = Flask(__name__)

# Connection details for MongoDB, MySQL, PostgreSQL
# mongo_db1 = pymongo.MongoClient("mongodb://localhost:27017")['database1']
# mongo_db2 = pymongo.MongoClient("mongodb://localhost:27018")['database2']

# mysql_db1 = mysql.connector.connect(
#     host="localhost",
#     user="user",
#     password="password",
#     database="database1"
# )

# mysql_db2 = mysql.connector.connect(
#     host="localhost",
#     user="user",
#     password="password",
#     database="database2"
# )

# postgres_db = psycopg2.connect(
#     host="localhost",
#     user="user",
#     password="password",
#     database="database"
# )

# Create a dictionary to map each database to its location
database_locations = {
    mongo_db1: {'latitude': 35.7707, 'longitude': -5.90783},  # mediouana tanger
    mongo_db2: {'latitude': 33.53885, 'longitude': -7.65672},  # ensem casablanca
    mysql_db1: {'latitude': 30.40696, 'longitude': -9.57708},  # sidi youssef agadir
    mysql_db2: {'latitude': 37.7749, 'longitude': -122.4194},  # Replace with actual coordinates
    postgres_db: {'latitude': 39.9526, 'longitude': -75.1652}  # Replace with actual coordinates
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

    return closest_db

def haversine(lat1, lon1, lat2, lon2):
    # Haversine formula to calculate distance between two points on the Earth
    R = 6371  # Radius of the Earth in kilometers

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (math.sin(math.radians(dlat) / 2) ** 2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * (math.sin(math.radians(dlon) / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def execute_query():
    query = request.form.get('query')
    user_location = get_user_location()
    
    # Determine the closest database based on user's location
    closest_db = get_closest_database(user_location['latitude'], user_location['longitude'])

    # Execute the query on the selected database
    result = closest_db.command('aggregate', 'collection1', pipeline=[{'$match': {'field': 'value'}}])

    return jsonify({'result': result})

def get_user_location():
    # Use geopy to get the user's location based on their IP address
    geolocator = Nominatim(user_agent="your_app_name")
    location = geolocator.geocode(request.remote_addr)
    
    if location:
        return {'latitude': location.latitude, 'longitude': location.longitude}
    else:
        return {'latitude': 0, 'longitude': 0}

if __name__ == '__main__':
    app.run(debug=True, threaded=True)