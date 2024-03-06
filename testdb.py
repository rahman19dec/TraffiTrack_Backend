# new db
import os
import urllib.parse as up
import psycopg2

from dotenv import load_dotenv

load_dotenv()

from datetime import datetime


detections = []
count = 0


up.uses_netloc.append("postgres")
url = up.urlparse(os.getenv("DATABASE_URL"))
conn = psycopg2.connect(database=url.path[1:],
user=url.username,
password=url.password,
host=url.hostname,
port=url.port
)
cursor = conn.cursor()

cursor.execute('SELECT * FROM detection_bytime')
rows = cursor.fetchall()
for row in rows:
    print(row, '\n')