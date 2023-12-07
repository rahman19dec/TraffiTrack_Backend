import cv2
import argparse

from ultralytics import YOLO
import supervision as sv
import numpy as np
from ultralytics.solutions import heatmap


ZONE_POLYGON = np.array([
    [0, 0],
    [0.5, 0],
    [0.5, 1],
    [0, 1]
])


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="YOLOv8 live")
    parser.add_argument(
        "--webcam-resolution", 
        default=[1920, 1080], 
        nargs=2, 
        type=int
    )
    args = parser.parse_args()
    return args


def main():

    cap = cv2.VideoCapture(1)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(cap.get(3)))
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(cap.get(4)))
    model = YOLO("yolov8l.pt")

    box_annotator = sv.BoxAnnotator(
        thickness=2,
        text_thickness=2,
        text_scale=1
    )

    zone_polygon = (ZONE_POLYGON * np.array([int(cap.get(3)),int(cap.get(4))])).astype(int)
    zone = sv.PolygonZone(polygon=zone_polygon, frame_resolution_wh=tuple([int(cap.get(3)),int(cap.get(4))]))
    zone_annotator = sv.PolygonZoneAnnotator(
        zone=zone, 
        color=sv.Color.red(),
        thickness=2,
        text_thickness=4,
        text_scale=2
    )
    heatmap_obj = heatmap.Heatmap()
    heatmap_obj.set_args(colormap=cv2.COLORMAP_CIVIDIS,
                         imw=cap.get(4),  # should same as im0 width
                         imh=cap.get(3),  # should same as im0 height
                         view_img=True)

    while True:
        ret, frame = cap.read()

        result = model(frame, agnostic_nms=True)[0]
        detections = sv.Detections.from_yolov8(result)
        labels = [
            f"{model.model.names[class_id]} {confidence:0.2f}"
            for _, confidence, class_id, _
            in detections
        ]
        frame = box_annotator.annotate(
            scene=frame, 
            detections=detections, 
            labels=labels
        )

        zone.trigger(detections=detections)
        frame = zone_annotator.annotate(scene=frame)
        results = model.track(frame, persist=True)
        frame = heatmap_obj.generate_heatmap(frame, tracks=results)
        
        cv2.imshow("yolov8", frame)

        if (cv2.waitKey(30) == 27):
            break


if __name__ == "__main__":
    main()
