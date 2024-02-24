# Creted by: Ahmad Imam (ahmadimam657@gmail.com)


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import sqlite3
import ast
from datetime import datetime
import cv2
import matplotlib.patches as patches
from ultralytics.solutions import heatmap

def create_heatmap(image, detections):
  
    """
    Create a heatmap on an image frame based on detections.

    Args:
    - image (numpy.ndarray): The input image frame.
    - detections (list): List of lists containing bounding box coordinates.

    Returns:
    - numpy.ndarray: The image frame with heatmap overlay.
    """
    # Create a figure and axis
    if image.shape[-1] == 3:  # OpenCV returns BGR images
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Create a figure and axis
    fig, ax = plt.subplots()
    ax.imshow(image)

    # Initialize heatmap matrix
    heatmap = np.zeros_like(image, dtype=np.float64)

    # Plot bounding boxes and update heatmap
    for idx, boxes in enumerate(detections):
        opacity = 1 / len(detections)  # Calculate opacity
        for box in boxes:
            x1, y1, x2, y2 = map(int, box)
            rect = patches.Rectangle((x1, y1), x2 - x1, y2 - y1, linewidth=1, edgecolor='red', facecolor='none', alpha=opacity)
            ax.add_patch(rect)

            # Update heatmap
            heatmap[y1:y2, x1:x2] += opacity

   # Apply colormap to heatmap
    heatmap = np.clip(heatmap, 0, 1)
    im = ax.imshow(heatmap, cmap='Reds', alpha=0.5)

    # Add colorbar
    cbar = plt.colorbar(im)
    cbar.set_label('Intensity')

    # Remove axis
    ax.axis('off')

    plt.show()



def get_object_counts(names,cursor,start_time = '2023-02-11 20:01:01' , end_time = '2025-02-11 20:01:01'):
    """
    Retrieves counts of objects detected within a specified time range from a SQLite database.

    Args:
    - start_time (str): Start time of the time range in 'YYYY-MM-DD HH:MM:SS' format.
    - end_time (str): End time of the time range in 'YYYY-MM-DD HH:MM:SS' format.

    Returns:
    - tuple: A tuple containing:
        - dict: A dictionary with object types as keys and lists of unique IDs as values.
        - int: Total count of objects detected within the time range.
        - dict: A dictionary with timestamps as keys and counts of objects detected at each timestamp as values.
    """
    # Connect to the SQLite database

    # Format datetime objects for SQL query
    start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')

    # Query the database based on the time range
    cursor.execute('''
        SELECT * FROM detection_bytime
        WHERE time BETWEEN ? AND ?
    ''', (start_time, end_time))

    rows = cursor.fetchall()

    # Process the data and count objects and class IDs
    count_objects = {i:[] for i in names}  # Dictionary to store objects and their IDs
    time_objects = {}  # Dictionary to store timestamp and count of objects detected
    for row in rows:
        for type_, id_ in zip(ast.literal_eval(row[4]), ast.literal_eval(row[5])):
            if id_ not in count_objects[type_]:
                count_objects[type_].append(id_)
    for row in rows:
        time_objects[row[1]] = len(ast.literal_eval(row[5]))
    total_objects = sum([len(i) for i in count_objects.values()])  # Total count of objects detected

    return count_objects, total_objects, time_objects


def plot_tracks(frame, results, track_history):
    """
    Plot tracks on a frame based on detected bounding boxes and track IDs.

    Args:
        frame (numpy.ndarray): Input frame/image.
        results (list): List of detection results.
        track_history (dict): Dictionary containing track history for each track ID.

    Returns:
        numpy.ndarray: Annotated frame with tracks plotted.
    """
    # Get the boxes and track IDs
    boxes = results[0].boxes.xywh.cpu()  # Extract bounding boxes
    track_ids = results[0].boxes.id.int().cpu().tolist()  # Extract track IDs

    # Plot the tracks
    for box, track_id in zip(boxes, track_ids):
        x, y, w, h = box
        track = track_history[track_id]
        track.append((float(x + w/2), float(y + h/2)))  # x, y center point
        if len(track) > 30:  # Retain tracks for 30 frames
            track.pop(0)

        # Draw the tracking lines
        points = np.array(track, dtype=np.int32).reshape((-1, 1, 2))
        cv2.polylines(frame, [points], isClosed=False, color=(230, 230, 230), thickness=10)

    return frame

def create_detection_table(cursor):
    """
    Create detection table if not exists.

    This function executes an SQL command to create a table named 'detection_bytime' if it doesn't exist.

    Args:
        cursor (sqlite3.Cursor): SQLite database cursor object.
    """
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS detection_bytime (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time TEXT,
            xyxy TEXT,
            confidence TEXT,
            class_id TEXT,s
            object_id TEXT
        )
    ''')
def insert_detection(cursor, detections):
    """
    Insert detection data into the 'detection_bytime' table.

    This function inserts detection data into the 'detection_bytime' table in an SQLite database.

    Args:
        cursor (sqlite3.Cursor): SQLite database cursor object.
        detections (list): List of detection entries, each containing time, xyxy, confidence, class_id, and object_id.

    Raises:
        sqlite3.Error: If there is an error executing the SQL command.
    """

    for entry in detections:
        # Extract data from the detection entry
        time = entry['time']
        xyxy = str(list(entry['xyxy']))
        confidence = str(list(entry['confidence']))
        class_id = str(list(entry['class_id']))
        object_id = str(list(entry['object_id']))

        # Insert data into the table
        try:
            cursor.execute('''
                INSERT INTO detection_bytime (time, xyxy, confidence, class_id, object_id)
                VALUES (?, ?, ?, ?, ?)
            ''', (time, xyxy, confidence, class_id, object_id))
        except sqlite3.Error as e:
            print("Error inserting data:", e)
            raise e
def plot_filtered_counts_over_time(times, counts):
    """
    Plot filtered object counts over time.

    This function filters time points based on changes in object counts and plots the results.

    Args:
    - times (list): A list of time points.
    - counts (list): A list of corresponding object counts.

    Returns:
    - None
    """
    filtered_times = [times[0]]  # Add the first time point
    filtered_counts = [counts[0]]  # Corresponding count
    for i in range(1, len(times)):
        if counts[i] != counts[i - 1]:  # If count changes from the previous time point
            filtered_times.append(times[i])
            filtered_counts.append(counts[i])

    plt.plot(filtered_times, filtered_counts, marker='o')
    plt.xlabel('Time')
    plt.ylabel('Total Objects Detected')
    plt.title('Traffic Objects Detected Over Time')
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
    plt.tight_layout()  # Adjust layout for better spacing
    plt.show()

def plot_non_zero_object_distribution(names,count_objects):
    """
    Plot distribution of non-zero confidence objects.

    This function filters out objects with 0.0% confidence and plots the distribution.

    Args:
    - count_objects (dict): A dictionary containing object types as keys and lists of unique IDs as values.

    Returns:
    - None
    """
    # Filter out objects with 0.0% confidence
    non_zero_sizes = {names[i]: len(ids) for i, ids in count_objects.items() if len(ids) > 0}

    # Plot pie chart
    plt.pie(non_zero_sizes.values(), labels=non_zero_sizes.keys(), autopct='%1.1f%%', startangle=90)
    plt.axis('equal')  # Equal aspect ratio ensures the pie is drawn as a circle.
    plt.title('Distribution of Traffic Objects')
    plt.show()
