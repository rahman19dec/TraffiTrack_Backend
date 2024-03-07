from ultralytics import YOLO
import cv2
import numpy as np
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
from collections import defaultdict
import time
from utils import *
import os
import urllib.parse as up
import psycopg2

from dotenv import load_dotenv

load_dotenv()

# Initialize YOLO model
MODEL = "best.pt"
model = YOLO(MODEL)

# Open the webcam
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Initialize heatmap object
heatmap_obj = heatmap.Heatmap()
heatmap_obj.set_args(colormap=cv2.COLORMAP_PARULA, imw=frame_width, imh=frame_height, shape="circle")

# Initialize variables
detections = []
track_history = defaultdict(lambda: [])

# Connect to ElephantSQL database
# up.uses_netloc.append("postgres")
# url = up.urlparse(os.getenv("DATABASE_URL"))
# conn = psycopg2.connect(database=url.path[1:],
# user=url.username,
# password=url.password,
# host=url.hostname,
# port=url.port
# )
conn = psycopg2.connect(dbname='jzvsjijt',user='jzvsjijt' ,host='cornelius.db.elephantsql.com' ,password=os.getenv('x'))


cursor = conn.cursor()

# Create detection table if it does not exist
create_detection_table(cursor)

# Function to update the Matplotlib plot with new frames
def update_plot(frame, scale=0.80):
    # Resize the frame to half its size (or any other scale factor)
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    resized_frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)

    cv2.imshow('output', resized_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
        return

try:
    while cap.isOpened():
        success, image = cap.read()
        if success:
            results = model.track(image, persist=True, tracker="bytetrack.yaml",imgsz=256)
            heatmap_frame = heatmap_obj.generate_heatmap(image.copy(), results)

            if results[0].boxes.id is not None:
                detections = [{'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                               'xyxy': list(results[0].boxes.xyxy.cpu().tolist()),
                               'confidence': list(results[0].boxes.conf.cpu().tolist()),
                               'class_id': list(results[0].boxes.cls.cpu().int().tolist()),
                               'object_id': list(map(int, list(results[0].boxes.id.cpu().tolist())))}]
                frame = results[0].plot()
                annotated_frame = plot_tracks(frame, results, track_history)
                update_plot(annotated_frame)
                try:
                    insert_detection(cursor, detections)
                    conn.commit()  # Commit the transaction
                except Exception as e:
                    print("Error inserting data into database:", e)
                    conn.rollback()  # Rollback the transaction in case of an error
            else:
                annotated_frame = None

            if annotated_frame is not None and annotated_frame.size > 0:
                pass
            else:
                pass

            plt.pause(0.5)

        else:
            break

except KeyboardInterrupt:
    pass

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()
