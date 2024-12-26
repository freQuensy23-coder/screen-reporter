import fastapi
import usecase
import models
from PIL import Image
import io
import base64
import uvicorn
from fastapi import FastAPI, Body
from pydantic import BaseModel

app = fastapi.FastAPI()


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/register")
async def register():
   user, error_message = usecase.register_user()
   if error_message and len(error_message) > 0:
       raise fastapi.HTTPException(status_code=500, detail=error_message)
   return {"user_id": user.id, "secret_key": user.secret_key}


@app.post("/login")
async def login(user_id: int, secret_key: str):
    if usecase.login(user_id, secret_key):
        return {"status": "ok"}
    else:
        raise fastapi.HTTPException(status_code=401, detail="Invalid secret key")
    

class ScreenshotRequest(BaseModel):
    user_id: int
    image_base64: str
    user_secret_key: str

@app.post("/screenshot")
async def process_image(request: ScreenshotRequest):
    if not usecase.login(request.user_id, request.user_secret_key):
        raise fastapi.HTTPException(status_code=401, detail="Invalid secret key")
    
    image = Image.open(io.BytesIO(base64.b64decode(request.image_base64)))
    result = await usecase.process_image(image)
    return {"result": result}
        
@app.get("/history")
async def get_history(user_id: int, user_secret_key: str, start_date: str, end_date: str):
    if not usecase.login(user_id, user_secret_key):
        raise fastapi.HTTPException(status_code=401, detail="Invalid secret key")
    history: list[models.ImageProcessingResult] = usecase.get_history(user_id, start_date, end_date)
    result = []
    for e in history:
        result.append({
            "openai_response": e.openai_response,
            "created_at": e.created_at.isoformat(),
        })

    return result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
