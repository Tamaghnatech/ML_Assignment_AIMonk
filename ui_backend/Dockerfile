FROM python:3.9-slim
WORKDIR /app
COPY ui_backend.py /app/
RUN pip install fastapi uvicorn requests python-multipart
CMD ["uvicorn", "ui_backend:app", "--host", "0.0.0.0", "--port", "8001"]
