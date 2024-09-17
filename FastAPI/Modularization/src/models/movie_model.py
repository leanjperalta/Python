from typing import List
from fastapi.responses import JSONResponse
from fastapi import Path, Query, APIRouter
from src.models.movie_model import Movie, MovieCreate, MovieUpdate #llamamos los modelos

movies: List[Movie] = [] #Indico que movies es una lista de tipo Movies

movie_router = APIRouter() #este router va a contener las rutas que tengan que ver con Movies

@movie_router.get('/', tags=['Movies']) # método get - ruta /movies
def get_movies() -> List[Movie]: #muestro una lista de tipo Movie (indico tipo de respuesta/schema)
#    return [movie.dict() for movie in movies] #devuelvo una lista, y por cada pelicula la convierto en un dict por cada movie en movies (lista)
     content = [movie.model_dump() for movie in movies]
     return JSONResponse(content=content, status_code=200)

@movie_router.get('/{id}', tags=['Movies']) # método get - ruta /movies
def get_movie(id: int = Path(gt=0)) -> Movie | dict: #muestro un objeto de tipo Movie (indico tipo de respuesta/schema), valido que el parametro id se mayor o igual a 0 (mod Path), devuelve una Movie o un diccionario en caso de no encontrar dato alguno
    for movie in movies:
        if movie.id == id: 
            return movie.dict() #convierto en dict
    
    return {} #devuelvo un objeto vacío ya que no hay mas listas para devolver (return [])

@movie_router.get('/by_category', tags=['Movies']) # método get - ruta /movies, modificamos ruta /by_category
def get_movie_by_category(category: str = Query(min_length=5)) -> Movie | dict: #Validación de parámetro query
      for movie in movies:
        if movie['category']== category:
            return movie.category
    
      return {}


@movie_router.post('/', tags=['Movies']) # método post - ruta /movies
def create_movie(movie: MovieCreate) -> List[Movie]: #parámetro movie del tipo Movie (clase creada)
    movies.append(movie) #añadimos movie 
    return [movie.dict() for movie in movies] #devuelvo una lista, y por cada pelicula la convierto en un dict por cada movie en movies (lista)

@movie_router.put('/{id}', tags=['Movies']) # método put - ruta /movies (operador id)
def update_movie(id: int, movie: MovieUpdate)-> List[Movie]:
    for item in movies:
        if item['id']== id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category
    return [movie.dict() for movie in movies] #devuelvo una lista, y por cada pelicula la convierto en un dict por cada movie en movies (lista)

@movie_router.delete('/{id}', tags=['Movies']) # método delete - ruta /movies (operador id)
def delete_movie(id:int) -> List[Movie]:
    for movie in movies:
        if movie['id'] == id:
            movies.remove(movie)
    
    return [movie.dict() for movie in movies] #devuelvo una lista, y por cada pelicula la convierto en un dict por cada movie en movies (lista)
            
    