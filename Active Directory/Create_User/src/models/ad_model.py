from pydantic import BaseModel, Field


class User(BaseModel):
    new_user_name: str #Optional[int] = None o se puede declarar id: int | None = None
    new_user_lastname: str
    
class UserCreate(BaseModel):
    new_user_name: str = Field(min_length=3, max_length=20) #Optional[int] = None o se puede declarar id: int | None = None
    new_user_lastname: str = Field(min_length=3, max_length=50)

    model_config = {    #Añado dentro del esquema valores por defecto en vez de hacerlo en Field()
        'json_schema_extra':{
            'example':{
                'new_user_name':'Ana',
                'new_user_lastname':'Perez',
            }
        }
    }
      
class UserUpdate(BaseModel):
    new_user_name: str
    new_user_lastname: str
    