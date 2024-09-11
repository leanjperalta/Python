from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse

app = FastAPI() 

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

def get_movies():
    return movies

@app.get('/movies/{id}', tags=['Movies']) # método get - ruta /movies

def get_movie(id: int):
    for movie in movies:
        if movie['id']== id:
            return movie
    
    return []

@app.get('/movies/', tags=['Movies']) # método get - ruta /movies

def get_movie_by_category(category: str, year: int):
      for movie in movies:
        if movie['category']== category:
            return movie
    
      return [] 


@app.post('/movies', tags=['Movies']) # método post - ruta /movies

def create_movie(id:int = Body(), 
                 title:str = Body(), 
                 overview:str = Body(), 
                 year:int  = Body(), 
                 rating:float = Body(),
                 category:str = Body()):
    movies.append({
        'id':id,
        'title':title,
        'overview':overview,
        'year':year,
        'rating':rating,
        'category':category
    })
    return movies

@app.put('/movies/{id}', tags=['Movies']) # método put - ruta /movies (operador id)

def update_movie(id: int,
                 title:str = Body(),  # Body request
                 overview:str = Body(), 
                 year:int  = Body(), 
                 rating:float = Body(),
                 category:str = Body()):
    for movie in movies:
        if movie['id']== id:
            movie['title'] = title
            movie['overview'] = overview
            movie['year'] = year
            movie['rating'] = rating
            movie['category'] = category
    return movies

@app.delete('/movies/{id}', tags=['Movies']) # método delete - ruta /movies (operador id)

def delete_movie(id:int):
    for movie in movies:
        if movie['id'] == id:
            movies.remove(movie)
    
    return movies
