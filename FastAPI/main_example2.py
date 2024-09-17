from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel,Field, validator
from typing import Optional, List
import datetime

#Versión usando validator module para validar datos y responder msg personalizados.
#Se reemplaza al método field, en este caso al elemento title en la clase CreateMovie

app = FastAPI() 

class Movie(BaseModel):
    id: int #Optional[int] = None o se puede declarar id: int | None = None
    title: str
    overview: str
    year: int
    rating: float
    category: str

class CreateMovie(BaseModel):
    id: int #Optional[int] = None o se puede declarar id: int | None = None
    title: str 
    overview: str = Field(min_length=5, max_length=50) #Valido condiciones de los datos
    year: int = Field(le=datetime.date.today().year) # el año debe ser menor o igual al año actual
    rating: float = Field(ge=0, le=10)
    category: str = Field(min_length=5, max_length=20)

    model_config = {    #Añado dentro del esquema valores por defecto en vez de hacerlo en Field()
        'json_schema_extra':{
            'example':{
                'id':1,
                'title': "My movie",
                'overview': "Esta pelicula se trata acerca de..",
                'year':2022,
                'rating':5,
                'category': "Comedia"
            }
        }
    }

    @validator('title')
    def validate_title(cls, value): #Valido title, recibo clase y valor de title.
        if len(value) < 5:
            raise ValueError('Title field must have a min. of 5 chars')
        if len(value) > 15:
            raise ValueError('Title field must have a max. of 15 chars')
        


class MovieUpdate(BaseModel):
    title: str
    overview: str
    year: int
    rating: float
    category: str


#app.title = "Mi primera app/FastAPI"

#app.version = "2.0.1"

# movies = [     # Lista de dicts
#     {
#         "id": 1,
#         "title": "Avatar",
#         "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
#         "year": "2009",
#         "rating": 7.8,
#         "category": "Acción"
#     },
#     {
#         "id": 2,
#         "title": "Avatar",
#         "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
#         "year": "2009",
#         "rating": 7.8,
#         "category": "Sci-fi"
#     }
# ]

movies: List[Movie] = [] #Indico que movies es una lista de tipo Movies

@app.get('/', tags=['Home']) # método get - ruta /

def home():
    return "Hola mundo"

@app.get('/movies', tags=['Movies']) # método get - ruta /movies

def get_movies() -> List[Movie]: #muestro una lista de tipo Movie (indico tipo de respuesta/schema)
    return [movie.dict() for movie in movies] #devuelvo una lista, y por cada pelicula la convierto en un dict por cada movie en movies (lista)

@app.get('/movies/{id}', tags=['Movies']) # método get - ruta /movies

def get_movie(id: int = Path(gt=0)) -> Movie | dict: #muestro un objeto de tipo Movie (indico tipo de respuesta/schema), valido que el parametro id se mayor o igual a 0 (mod Path), devuelve una Movie o un diccionario en caso de no encontrar dato alguno
    for movie in movies:
        if movie.id == id: 
            return movie.dict() #convierto en dict
    
    return {} #devuelvo un objeto vacío ya que no hay mas listas para devolver (return [])

@app.get('/movies/', tags=['Movies']) # método get - ruta /movies

def get_movie_by_category(category: str = Query(min_length=5)) -> Movie | dict: #Validación de parámetro query
      for movie in movies:
        if movie['category']== category:
            return movie.category
    
      return {}


@app.post('/movies', tags=['Movies']) # método post - ruta /movies

def create_movie(movie: CreateMovie) -> List[Movie]: #parámetro movie del tipo Movie (clase creada)
    movies.append(movie) #añadimos movie 
    return [movie.dict() for movie in movies] #devuelvo una lista, y por cada pelicula la convierto en un dict por cada movie en movies (lista)

@app.put('/movies/{id}', tags=['Movies']) # método put - ruta /movies (operador id)

def update_movie(id: int, movie: MovieUpdate)-> List[Movie]:
    for item in movies:
        if item['id']== id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category
    return [movie.dict() for movie in movies] #devuelvo una lista, y por cada pelicula la convierto en un dict por cada movie en movies (lista)

@app.delete('/movies/{id}', tags=['Movies']) # método delete - ruta /movies (operador id)

def delete_movie(id:int) -> List[Movie]:
    for movie in movies:
        if movie['id'] == id:
            movies.remove(movie)
    
    return [movie.dict() for movie in movies] #devuelvo una lista, y por cada pelicula la convierto en un dict por cada movie en movies (lista)
            
    

                
