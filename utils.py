# Creted by: Ahmad Imam (ahmadimam657@gmail.com)


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import sqlite3
import ast
from datetime import datetime


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
    heatmap = np.zeros_like(image, dtype=np.float)

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



def get_object_counts(start_time, end_time):
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
    conn = sqlite3.connect('predictions_database.db')
    cursor = conn.cursor()

    # Format datetime objects for SQL query
    start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')

    # Query the database based on the time range
    cursor.execute('''
        SELECT * FROM predictions_bytime
        WHERE time BETWEEN ? AND ?
    ''', (start_time, end_time))

    rows = cursor.fetchall()

    # Close the connection
    conn.close()

    # Process the data and count objects and class IDs
    count_objects = {i:[] for i in model.names}  # Dictionary to store objects and their IDs
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