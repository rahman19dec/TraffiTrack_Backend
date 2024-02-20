from flask import Flask, jsonify, request
import urllib.parse as up
import psycopg2

from dotenv import load_dotenv

load_dotenv()
import os, ast 
from collections import Counter

app = Flask(__name__)

classes = {0: 'person', 1: 'bicycle', 2: 'car', 3: 'motorcycle', 
            4: 'bus', 5: 'truck'}

# average carbon per km for each class
carbon_index = {'2':120, '3':80, '4':250, '5':400}
# average travel time for each class
travel_index = {'2':50, '3':30, '4':200, '5':150}


@app.route('/classes', methods=['GET'])
def get_classes():
    return jsonify(classes), 500


def read_db(command):
    app_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(app_dir, os.pardir))
    db_path = os.path.join(parent_dir, 'detection_database.db')
    
    try:
        conn = psycopg2.connect(dbname='jzvsjijt',user='jzvsjijt' ,host='cornelius.db.elephantsql.com' ,password=os.getenv('x'))
        cursor = conn.cursor()

        # Execute a query to fetch data from the database
        cursor.execute(command)
        data = cursor.fetchall()

        # Close the database cursor and connection
        cursor.close()
        conn.close()

        # Return the data as JSON
        return data
    except Exception as error:
        return {'message':error}


@app.route('/all', methods=['GET'])
def get_all_data():
    command = 'SELECT * FROM detection_bytime'
    return jsonify(read_db(command))



@app.route('/count', methods=['GET'])
def get_count():
    # Get optional parameters from the request
    # example: http://127.0.0.1:5000/count?from_time=2024-02-24%2015:00:00&to_time=2025-02-25%2016:00:00
    from_time = request.args.get('from_time')
    to_time = request.args.get('to_time')
    print(from_time, to_time)
    
    # Construct the base SQL command
    command = 'SELECT * FROM detection_bytime'
    
    # Add WHERE clause to filter by time range if both from_time and to_time are provided
    if from_time and to_time:
        command += f" WHERE time BETWEEN '{from_time.replace('T',' ')}' AND '{to_time.replace('T',' ')}'"
    elif from_time:
        command += f" WHERE time >= '{from_time.replace('T',' ')}'"
    elif to_time:
        command += f" WHERE time <= '{to_time.replace('T',' ')}'"
    
    # Execute the database query
    data = read_db(command)
    
    # Process the data to calculate counts
    count = {i: 0 for i, _ in classes.items()}
    last_count = count.copy()

    for arr in data:
        rec_count = {element: c for element, c in Counter(ast.literal_eval(arr[4])).items()}
        rec_count = {i: rec_count.get(i, 0) for i,_ in classes.items()}

        for k, v in rec_count.items():
            if last_count[k] < v:
                count[k] += v - last_count[k]

        # print(rec_count, last_count, count)
        last_count.update(rec_count)


    # Return the counts as JSON
    return jsonify(count)


@app.route('/stat', methods=['GET'])
def get_stat():
    # Get optional parameters from the request
    # example: http://127.0.0.1:5000/stat?from_time=2024-02-24%2015:00:00&to_time=2025-02-25%2016:00:00
    from_time = request.args.get('from_time')
    to_time = request.args.get('to_time')
    
    # Construct the base SQL command
    command = 'SELECT * FROM detection_bytime'
    
    # Add WHERE clause to filter by time range if both from_time and to_time are provided
    if from_time and to_time:
        command += f" WHERE time BETWEEN '{from_time.replace('T',' ')}' AND '{to_time.replace('T',' ')}'"
    elif from_time:
        command += f" WHERE time >= '{from_time.replace('T',' ')}'"
    elif to_time:
        command += f" WHERE time <= '{to_time.replace('T',' ')}'"
    
    # Execute the database query
    data = read_db(command)
    
    # Process the data to calculate counts
    count = {i: 0 for i, _ in classes.items()}
    last_count = count.copy()
    line_count = {i[1]: {j: 0 for j, _ in classes.items()} for i in data}

    for dec in data:
        for i in eval(dec[-2]):
            line_count[dec[1]][i]+=1

    return jsonify(line_count)


@app.route('/carbon', methods=['GET'])
def get_carbon():
    from_time = request.args.get('from_time')
    to_time = request.args.get('to_time')

    command = 'SELECT * FROM detection_bytime'

    if from_time and to_time:
        command += f" WHERE time BETWEEN '{from_time.replace('T',' ')}' AND '{to_time.replace('T',' ')}'"
    elif from_time:
        command += f" WHERE time >= '{from_time.replace('T',' ')}'"
    elif to_time:
        command += f" WHERE time <= '{to_time.replace('T',' ')}'"

    data = read_db(command)
    
    count = {i: 0 for i, _ in classes.items()}
    last_count = count.copy()

    for arr in data:
        rec_count = {element: c for element, c in Counter(ast.literal_eval(arr[4])).items()}
        rec_count = {i: rec_count.get(i, 0) for i,_ in classes.items()}

        for k, v in rec_count.items():
            if last_count[k] < v:
                count[k] += v - last_count[k]

        # print(rec_count, last_count, count)
        last_count.update(rec_count)
    
    carbon = {i:0 for i in classes.keys()}
    total_carbon = 0

    for k, v in count.items():
        carbon[k] = v * carbon_index.get(str(k), 0) * travel_index.get(str(k), 0)/1000000
        total_carbon += v * carbon_index.get(str(k), 0) * travel_index.get(str(k), 0)/1000000

    print(carbon)
    return jsonify({'classes': carbon, 'total_carbon': total_carbon})
    
    

if __name__ == '__main__':
    app.run(debug=True)
