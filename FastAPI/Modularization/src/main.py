from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel,Field, validator
from typing import Optional, List
from src.routers.movie_router import movie_router
import datetime

#Versión usando validator module para validar datos y responder msg personalizados.
#Se reemplaza al método field, en este caso al elemento title en la clase CreateMovie

app = FastAPI() 

@app.get('/', tags=['Home']) # método get - ruta /

def home():
    return "Hola mundo"

app.include_router(prefix="/movies", router=movie_router) #llama las rutas Movies a través de movie_router (APIRouter)



                
