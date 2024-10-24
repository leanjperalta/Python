from fastapi import FastAPI
from src.routers.ad_router import aduser_router

app = FastAPI() 

@app.get('/', tags=['Home']) # método get - ruta /

def home():
    return "Nada para hacer aqui"

app.include_router(prefix="/aduser", router=aduser_router) #llama las rutas aduser a través de aduser_router (APIRouter), e indico el prefijo

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)