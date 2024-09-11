from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI() 

class Movie(BaseModel):
    id: int #Optional[int] = None o se puede declarar id: int | None = None
    title: str
    overview: str
    year: int
    rating: float
    category: str

class MovieUpdate(BaseModel):
    title: str
    overview: str
    year: int
    rating: float
    category: str


#app.title = "Mi primera app/FastAPI"

#app.version = "2.0.1"

movies = [     # Lista de dicts
    {
        "id": 1,
        "title": "Avatar",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        "year": "2009",
        "rating": 7.8,
        "category": "Acción"
    },
    {
        "id": 2,
        "title": "Avatar",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        "year": "2009",
        "rating": 7.8,
        "category": "Sci-fi"
    }
]

@app.get('/', tags=['Home']) # método get - ruta /

def home():
    return "Hola mundo"

@app.get('/movies', tags=['Movies']) # método get - ruta /movies

def get_movies() -> List[Movie]: #muestro una lista de tipo Movie (indico tipo de respuesta/schema)
    return movies

@app.get('/movies/{id}', tags=['Movies']) # método get - ruta /movies

def get_movie(id: int) -> Movie: #muestro un objeto de tipo Movie (indico tipo de respuesta/schema)
    for movie in movies:
        if movie['id']== id:
            return movie
    
    return []

@app.get('/movies/', tags=['Movies']) # método get - ruta /movies

def get_movie_by_category(category: str, year: int) -> Movie:
      for movie in movies:
        if movie['category']== category:
            return movie
    
      return [] 


@app.post('/movies', tags=['Movies']) # método post - ruta /movies

def create_movie(movie: Movie) -> List[Movie]: #parámetro movie del tipo Movie (clase creada)
    movies.append(movie.dict()) #añadimos movie y lo convertimos en dict que es lo que requiere el método append
    return movies

@app.put('/movies/{id}', tags=['Movies']) # método put - ruta /movies (operador id)

def update_movie(id: int, movie: MovieUpdate)-> List[Movie]:
    for item in movies:
        if item['id']== id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category
    return movies

@app.delete('/movies/{id}', tags=['Movies']) # método delete - ruta /movies (operador id)

def delete_movie(id:int) -> List[Movie]:
    for movie in movies:
        if movie['id'] == id:
            movies.remove(movie)
    
    return movies
            
    

                
