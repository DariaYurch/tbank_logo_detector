from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import List, Optional
from ultralytics import YOLO
from PIL import Image, ImageDraw
import io, base64


class BoundingBox(BaseModel):
    """Абсолютные координаты BoundingBox"""
    x_min: int = Field(..., description="Левая координата", ge=0)
    y_min: int = Field(..., description="Верхняя координата", ge=0)
    x_max: int = Field(..., description="Правая координата", ge=0)
    y_max: int = Field(..., description="Нижняя координата", ge=0)

class Detection(BaseModel):
    """Результат детекции одного логотипа"""
    bbox: BoundingBox = Field(..., description="Результат детекции")

class DetectionResponse(BaseModel):
    """Ответ API с результатами детекции"""
    detections: List[Detection] = Field(..., description="Список найденных логотипов")

class ErrorResponse(BaseModel):
    """Ответ при ошибке"""
    error: str = Field(..., description="Описание ошибки")
    detail: Optional[str] = Field(None, description="Дополнительная информация")


app = FastAPI(title="Т-Bank Logo Detector")
model = YOLO("best_11.pt")
app.mount("/static", StaticFiles(directory="static"), name="static")



@app.get("/", response_class=HTMLResponse)
async def index():
    with open("index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

#эндпоинт согласно кейсу:
@app.post("/detect", response_model=DetectionResponse, responses={400: {"model": ErrorResponse}})
async def detect_logo(file: UploadFile = File(...)):
    try:
        image_b = await file.read()
        image = Image.open(io.BytesIO(image_b)).convert("RGB")

        results = model.predict(image) #обрабатываем картинку моделью

        detections = []
        for r in results: #проходимся по всем найденным на изображении логотипам Т-Банка
            for box in r.boxes:
                x_min, y_min, x_max, y_max = box.xyxy[0].tolist()
                detections.append(
                    Detection(
                        bbox=BoundingBox(
                            x_min=int(x_min),
                            y_min=int(y_min),
                            x_max=int(x_max),
                            y_max=int(y_max),
                        )
                    )
                )
        return DetectionResponse(detections=detections)

    except Exception as e:
        return ErrorResponse(error="Detection failed", detail=str(e))

#для вывода картинки на страницу
@app.post("/detect_ui")
async def detect_ui(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        results = model.predict(image)

        detections = []
        draw = ImageDraw.Draw(image)

        for r in results:
            for box in r.boxes:
                x_min, y_min, x_max, y_max = box.xyxy[0].tolist()
                bbox = BoundingBox(
                    x_min=int(x_min),
                    y_min=int(y_min),
                    x_max=int(x_max),
                    y_max=int(y_max))
                detections.append(Detection(bbox=bbox))
                draw.rectangle([x_min, y_min, x_max, y_max], outline="lime", width=3) #отрисовываем найденные лого
        #конвертируем картинку в base64, чтобы не хранить ее на диске
        buf = io.BytesIO()
        image.save(buf, format="JPEG")
        img_str = base64.b64encode(buf.getvalue()).decode("utf-8")
        return {
            "detections": [d.dict() for d in detections],
            "image": f"data:image/jpeg;base64,{img_str}",
        }

    except Exception as err:
        return {"error": "Detection failed", "detail": str(err)}
