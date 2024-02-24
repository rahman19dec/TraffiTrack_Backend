from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

def read_db(command):
    try:
        conn = sqlite3.connect('../detection_database.db')
        cursor = conn.cursor()

        # Execute a query to fetch data from the database
        cursor.execute(command)
        data = cursor.fetchall()

        # Close the database cursor and connection
        cursor.close()
        conn.close()

        # Return the data as JSON
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/all', methods=['GET'])
def get_all_data():
    command = 'SELECT * FROM detection_bytime'
    return read_db(command)











@app.route('/classes', methods=['GET'])
def get_classes():
    d = {0: 'person', 1: 'bicycle', 2: 'car', 3: 'motorcycle', 
            4: 'bus', 5: 'truck'}
    return jsonify(d), 500

if __name__ == '__main__':
    app.run(debug=True)
