from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import base64
from PIL import Image
from io import BytesIO

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
  return templates.TemplateResponse("image_template.html", {"request":request})


@app.post("/convert/")
async def convert_base64_to_image(request: Request, base64_str: str = Form(...)):
    try:
        # Decode base64 string to bytes
        img_bytes = base64.b64decode(base64_str)

        # Open the image
        img = Image.open(BytesIO(img_bytes))

        # Render to template
        return templates.TemplateResponse("image_template.html", {"request": request, "image": img})

    except Exception as e:
        raise HTTPException(status_code=400, detail="Failed to process image")


