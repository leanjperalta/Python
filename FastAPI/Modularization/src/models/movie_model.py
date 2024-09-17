import datetime
from pydantic import BaseModel, Field, validator


class Movie(BaseModel):
    id: int #Optional[int] = None o se puede declarar id: int | None = None
    title: str
    overview: str
    year: int
    rating: float
    category: str

class MovieCreate(BaseModel):
    id: int #Optional[int] = None o se puede declarar id: int | None = None
    title: str = Field(min_length=5, max_length=15)
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

    # @validator('title')
    # def validate_title(cls, value): #Valido title, recibo clase y valor de title.
    #     if len(value) < 5:
    #         raise ValueError('Title field must have a min. of 5 chars')
    #     if len(value) > 15:
    #         raise ValueError('Title field must have a max. of 15 chars')
        
class MovieUpdate(BaseModel):
    title: str
    overview: str
    year: int
    rating: float
    category: str