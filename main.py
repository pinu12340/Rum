import PIL.Image
from fastapi import FastAPI, Response
from pydantic import BaseModel
import base64
from io import BytesIO
import PIL
from rembg import remove
from fastapi.middleware.cors import CORSMiddleware

class ImgFile(BaseModel):
    imgString : str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def helloworld():
    return {"message": "congrats"}



@app.post("/remove_background")
def background_remover(file : ImgFile):
    imgString = file.imgString
    imgBin = base64.b64decode(imgString)
    imgBytes = BytesIO(imgBin)
    pilImg = PIL.Image.open(imgBytes)
    backgroundremoveImage = remove(pilImg)
    outBytes =  BytesIO()
    backgroundremoveImage.save(outBytes,"png")
    return Response(base64.b64encode(outBytes.getvalue()),status_code=200,media_type="text/base64")
