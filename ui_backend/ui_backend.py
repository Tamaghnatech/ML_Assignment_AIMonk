from fastapi import FastAPI, Form, Request, File, UploadFile
from fastapi.responses import HTMLResponse
import requests

app = FastAPI()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<body>
<h2>Upload Image for Object Detection</h2>
<form action="/upload/" method="post" enctype="multipart/form-data">
  <input type="file" name="file" accept="image/*"><br><br>
  <input type="submit" value="Upload">
</form>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def home():
    return HTML_TEMPLATE

@app.post("/upload/")
async def upload(file: UploadFile = File(...)):
    # Send the uploaded image to AI Backend
    ai_backend_url = "http://ai_backend:8000/detect/"
    files = {"file": file.file}
    response = requests.post(ai_backend_url, files=files)
    return response.json()
