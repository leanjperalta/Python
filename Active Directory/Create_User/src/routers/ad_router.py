
from typing import List
from fastapi.responses import JSONResponse
from fastapi import Path, Query, APIRouter
from src.models.ad_model import User, UserCreate, UserUpdate #llamamos los modelos

users: List[User] = [] #Indico que users es una lista de tipo Users

aduser_router = APIRouter() #este router va a contener las rutas que tengan que ver con Movies

@aduser_router.get('/', tags=['User']) # método get - ruta /User
def get_users() -> List[User]: #muestro una lista de tipo User (indico tipo de respuesta/schema)
#    return [movie.dict() for movie in movies] #devuelvo una lista, y por cada pelicula la convierto en un dict por cada user en users (lista)
     content = [user.model_dump() for user in users]
     return JSONResponse(content=content, status_code=200)

@aduser_router.get('/{id}', tags=['User']) # método get - ruta /User
def get_users(id: int = Path(gt=0)) -> User | dict: #muestro un objeto de tipo User (indico tipo de respuesta/schema), valido que el parametro id se mayor o igual a 0 (mod Path), devuelve una User o un diccionario en caso de no encontrar dato alguno
    for user in users:
        if user.id == id: 
            return user.dict() #convierto en dict
    
    return {} #devuelvo un objeto vacío ya que no hay mas listas para devolver (return [])

@aduser_router.post('/', tags=['User'], status_code=201)
def create_user(user: UserCreate) -> User:
    new_user = user.model_dump()
    users.append(new_user)
    return JSONResponse(content=new_user, status_code=201)

@aduser_router.put('/{id}', tags=['User'])
def update_user(id: int, user: UserUpdate) -> User:
    for user in users:
        if user.id == id:
            user.new_user_name = user.new_user_name
            user.new_user_lastname = user.new_user_lastname
            return user.dict()
    return {}