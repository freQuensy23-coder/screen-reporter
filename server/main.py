import fastapi
from . import usecase
from . import models
from PIL import Image
import io
import base64

app = fastapi.FastAPI()


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/register")
async def register():
   user = await usecase.register_user()
   return {"user_id": user.id, "secret_key": user.secret_key}


@app.post("/login")
async def login(user_id: int, secret_key: str):
    if usecase.login(user_id, secret_key):
        return {"status": "ok"}
    else:
        raise fastapi.HTTPException(status_code=401, detail="Invalid secret key")
    

@app.post("/screenshot")
async def process_image(user_id: int, image_base64: str, user_secret_key: str):
    if not usecase.login(user_id, user_secret_key):
        raise fastapi.HTTPException(status_code=401, detail="Invalid secret key")
    
    image = Image.open(io.BytesIO(base64.b64decode(image_base64)))
    result = await usecase.process_image(image)
    return {"result": result}
        
@app.get("/history")
async def get_history(user_id: int, user_secret_key: str, start_date: str, end_date: str):
    if not usecase.login(user_id, user_secret_key):
        raise fastapi.HTTPException(status_code=401, detail="Invalid secret key")
    history: list[models.ImageProcessingResult] = await usecase.get_history(user_id, start_date, end_date)
    result = []
    for e in history:
        result.append({
            "openai_response": e.openai_response,
            "created_at": e.created_at.isoformat(),
        })

    return result
