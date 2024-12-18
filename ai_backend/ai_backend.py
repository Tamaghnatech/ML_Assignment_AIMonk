from fastapi import FastAPI, File, UploadFile
import cv2
import numpy as np
from ultralytics import YOLO
import json
import os

app = FastAPI()
model = YOLO('yolov3u.pt')  # Use YOLOv3u for compatibility

@app.post("/detect")
async def detect(file: UploadFile = File(...)):
    # Define class names mapping
    class_names = {
        0: "person",
        16: "dog",
        24: "backpack",
        # Add other mappings here as needed
    }

    # Reading the uploaded image file
    image = np.frombuffer(file.file.read(), np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    # Perform object detection
    results = model.predict(image)
    detections = []

    for result in results:
        for box in result.boxes:  # Access each detected box
            detections.append({
                "class": class_names.get(int(box.cls), "unknown"),  # Map class ID to name
                "confidence": float(box.conf),
                "box": box.xyxy[0].tolist()  # Bounding box coordinates
            })

    # Save annotated image with bounding boxes
    output_path = "output/"
    os.makedirs(output_path, exist_ok=True)
    output_image_path = os.path.join(output_path, "output_image.jpg")
    annotated_image = results[0].plot()  # Get annotated image
    cv2.imwrite(output_image_path, annotated_image)

    # Save JSON output
    json_path = os.path.join(output_path, "detections.json")
    with open(json_path, "w") as json_file:
        json.dump({"detections": detections}, json_file)

    return {"message": "Success", "detections": detections}
