# Creted by: Ahmad Imam (ahmadimam657@gmail.com)



from ultralytics import YOLO
import cv2
import numpy as np
import sqlite3
import ast
from datetime import datetime
import matplotlib.pyplot as plt
from collections import defaultdict

MODEL = "best.pt"
model = YOLO(MODEL)

# Open the video file
video_path = "test_video.mp4"
video_name = 'results.avi'
cap = cv2.VideoCapture(video_path)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
video = cv2.VideoWriter(video_name, 0, 1, (frame_width,frame_height))
detections = []
count = 0
track_history = defaultdict(lambda: [])
while cap.isOpened():
  success,image = cap.read()
  if success:
    results = model.track(image, persist=True,tracker="bytetrack.yaml")
    if results[0].boxes.id != None:
      detections.append({'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'xyxy':list(results[0].boxes.xyxy.cpu().tolist()),
      'confidence':list(results[0].boxes.conf.cpu().tolist()),
      'class_id':list(results[0].boxes.cls.cpu().int().tolist()),
      'object_id':list(map(int,list(results[0].boxes.id.cpu().tolist())))})
    frame = results[0].plot()
    annotated_frame = plot_tracks(frame, results, track_history)
    video.write(annotated_frame)
  else:
    break
