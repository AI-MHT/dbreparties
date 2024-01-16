from flask import Flask, render_template, request, jsonify
import mysql.connector
import os  # Add this import

app = Flask(__name__)

# Set the path to the templates folder explicitly
template_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "templates"))
app = Flask(__name__, template_folder=template_folder_path)

# MySQL database configuration
cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="store"
)

# Function to execute SQL queries
def execute_query(query):
    try:
        cursor = cnx.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result
    except Exception as e:
        return str(e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute-sql', methods=['POST'])
def execute_sql():
    try:
        sql_query = request.form['query']
        
        # Execute the SQL query
        result = execute_query(sql_query)

        # Return the result as JSON
        return render_template('index.html', query=sql_query, result=result)
    except Exception as e:
        return render_template('index.html', query=sql_query, error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
