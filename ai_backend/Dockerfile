FROM python:3.9-slim

# Installed system dependencies for OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0

WORKDIR /app
COPY ai_backend.py /app/

# Installed Python dependencies
RUN pip install fastapi uvicorn torch torchvision ultralytics opencv-python python-multipart

CMD ["uvicorn", "ai_backend:app", "--host", "0.0.0.0", "--port", "8000"]
