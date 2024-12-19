from fastapi import FastAPI, File, UploadFile
import cv2
import numpy as np
from ultralytics import YOLO
import json
import os

app = FastAPI()
model = YOLO('yolov3u.pt')  # Using YOLOv3u for compatibility

@app.post("/detect")
async def detect(file: UploadFile = File(...)):
    # Reading the uploaded image file
    image = np.frombuffer(file.file.read(), np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    
    # Perform object detection
    results = model.predict(image)
    detections = []
    
    # Draw bounding boxes on the image
    annotated_image = image.copy()
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()  # Get bounding box coordinates
            confidence = box.conf[0].item()  # Get confidence score
            class_id = box.cls[0].item()  # Get class ID
            
            # Draw rectangle and label
            label = model.names[int(class_id)]  # Get class name
            cv2.rectangle(annotated_image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(annotated_image, f"{label} {confidence:.2f}", 
                        (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            # Append detection to results
            detections.append({
                "label": label,
                "confidence": float(confidence),
                "box": [x1, y1, x2, y2]
            })

    # Save the annotated image
    output_path = "output/"
    os.makedirs(output_path, exist_ok=True)
    output_image_path = os.path.join(output_path, "output_image.jpg")
    cv2.imwrite(output_image_path, annotated_image)
    
    # Save JSON output
    json_path = os.path.join(output_path, "detections.json")
    with open(json_path, "w") as json_file:
        json.dump({"detections": detections}, json_file)
        
    return {
        "message": "Success",
        "detections": detections,
        "image_path": output_image_path
    }
