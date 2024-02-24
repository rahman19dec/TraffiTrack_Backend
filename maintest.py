# Creted by: Ahmad Imam (ahmadimam657@gmail.com)



from ultralytics import YOLO
import cv2
import numpy as np
import sqlite3
import ast
from datetime import datetime
import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
from collections import defaultdict
# from main_utils import *
from utils import *



MODEL = "best.pt"
model = YOLO(MODEL)


#cap = cap = cv2.VideoCapture(0)
#cap.set(3, 640)
#cap.set(4, 480)
#frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#heatmap_obj = heatmap.Heatmap()
#heatmap_obj.set_args(colormap=cv2.COLORMAP_PARULA, imw=frame_width, imh=frame_height, shape="circle")



detections = []
count = 0
track_history = defaultdict(lambda: [])



conn = sqlite3.connect('predictions_database.db')
cursor = conn.cursor()


# Create predictions table if it does not exit
# create_predictions_table(cursor)

# while cap.isOpened():
#   success,image = cap.read()
#   if success:
#     results = model.track(image, persist=True,tracker="bytetrack.yaml")
#     heatmap_frame = heatmap_obj.generate_heatmap(image.copy(), results)
#     cv2.imshow("Heatmap", heatmap_frame)
#     if results[0].boxes.id != None:
#       detections = [{'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'xyxy':list(results[0].boxes.xyxy.cpu().tolist()),
#       'confidence':list(results[0].boxes.conf.cpu().tolist()),
#       'class_id':list(results[0].boxes.cls.cpu().int().tolist()),
#       'object_id':list(map(int,list(results[0].boxes.id.cpu().tolist())))}]
#       frame = results[0].plot()
#       annotated_frame = plot_tracks(frame, results, track_history)
#       insert_predictions(cursor, detections)
#     else:
#       annotated_frame = None
#     if annotated_frame is not None and annotated_frame.size > 0:
#       cv2.imshow("Track", annotated_frame)
#     else:
#       cv2.imshow("Track", image)
#   else:
#     break

cursor.execute('SELECT * FROM predictions_bytime')
rows = cursor.fetchall()
print(rows)



count_objects,total_objects,time_objects = get_object_counts(model.names,cursor)


print(f"Total objects detected: {total_objects}")
print(f"type wise count:", {model.names[k]:len(v) for k,v in count_objects.items()})


times = list(time_objects.keys())
counts = list(time_objects.values())

# plot_filtered_counts_over_time(times, counts)
plot_filtered_counts_over_time(times, counts)
plot_non_zero_object_distribution(model.names,count_objects)


dt = [i['xyxy'] for i in detections]
#create_heatmap(cv2.imread('frame0.jpg','L'),dt)
