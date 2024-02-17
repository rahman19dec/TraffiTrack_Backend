# Creted by: Ahmad Imam (ahmadimam657@gmail.com)

from ultralytics import YOLO
import cv2
import numpy as np
import sqlite3
from sqlite3 import Error
import ast
from datetime import datetime
from collections import defaultdict
from utils import *

# Function to create a connection to the SQLite3 database
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to SQLite version: {sqlite3.version}")
        return conn
    except Error as e:
        print(e)
    return conn

# Function to create the predictions table if it does not exist
def create_predictions_table(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS predictions_bytime
                      (id INTEGER PRIMARY KEY,
                       time TEXT,
                       xyxy TEXT,
                       confidence TEXT,
                       class_id TEXT,
                       object_id TEXT)''')

# Function to insert predictions into the database
def insert_predictions(cursor, detections):
    for detection in detections:
        time = detection['time']
        xyxy = str(detection['xyxy'])
        confidence = str(detection['confidence'])
        class_id = str(detection['class_id'])
        object_id = str(detection['object_id'])
        cursor.execute('''INSERT INTO predictions_bytime
                          (time, xyxy, confidence, class_id, object_id)
                          VALUES (?, ?, ?, ?, ?)''',
                       (time, xyxy, confidence, class_id, object_id))

# Function to track objects and store predictions
def track_and_store_predictions(cap, model, cursor):
    detections = []
    track_history = defaultdict(lambda: [])
    while cap.isOpened():
        success, image = cap.read()
        if success:
            results = model.track(image, persist=True, tracker="bytetrack.yaml")
            if results[0].boxes.id is not None:
                detections.append({
                    'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'xyxy': list(results[0].boxes.xyxy.cpu().tolist()),
                    'confidence': list(results[0].boxes.conf.cpu().tolist()),
                    'class_id': list(results[0].boxes.cls.cpu().int().tolist()),
                    'object_id': list(map(int, list(results[0].boxes.id.cpu().tolist())))
                })
                frame = results[0].plot()
                annotated_frame = plot_tracks(frame, results, track_history)
            else:
                annotated_frame = None
            if annotated_frame is not None and annotated_frame.size > 0:
                video_name_track.write(annotated_frame)
            else:
                video_name_track.write(image)
        else:
            break

    # Insert predictions into the database
    insert_predictions(cursor, detections)

# Main function
if __name__ == "__main__":
    # Model and video settings
    MODEL = "best.pt"
    model = YOLO(MODEL)
    video_path = "test_video.mp4"
    video_name_track = 'track_result.avi'
    heatmap_video_writer = cv2.VideoWriter('heatmap_result.avi', 0, 30, (frame_width, frame_height))
    heatmap_obj = heatmap.Heatmap()
    heatmap_obj.set_args(colormap=cv2.COLORMAP_PARULA, imw=frame_width, imh=frame_height, shape="circle")

    # Open video capture
    cap = cv2.VideoCapture(video_path)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    video_name_track = cv2.VideoWriter(video_name_track, 0, 30, (frame_width, frame_height))

    # Connect to SQLite database
    conn = create_connection("predictions_database.db")
    cursor = conn.cursor()

    # Track objects and store predictions
    track_and_store_predictions(cap, model, cursor)

    # Close database connection
    conn.commit()
    conn.close()
