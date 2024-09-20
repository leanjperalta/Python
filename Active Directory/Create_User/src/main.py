from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel,Field
from typing import Optional, List
from src.routers.ad_router import aduser_router

app = FastAPI() 

@app.get('/', tags=['Home']) # método get - ruta /

def home():
    return "Nada para hacer aqui"

app.include_router(prefix="/aduser", router=aduser_router) #llama las rutas aduser a través de aduser_router (APIRouter), e indico el prefijo
