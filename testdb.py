# new db
import sqlite3
from datetime import datetime


detections = []
count = 0


conn = sqlite3.connect('detection_database.db')
cursor = conn.cursor()

cursor.execute('SELECT * FROM detection_bytime')
rows = cursor.fetchall()
for row in rows:
    print(row, '\n')