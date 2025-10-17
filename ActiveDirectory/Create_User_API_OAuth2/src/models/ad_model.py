from pydantic import BaseModel, Field

  
class UserCreate(BaseModel):
    new_user_name: str = Field(min_length=3, max_length=30) #Optional[int] = None o se puede declarar id: int | None = None
    new_user_lastname: str = Field(min_length=3, max_length=50) #Optional[str] = None o se puede declarar new_user_password: str | None = None
    new_username: str = Field(min_length=3, max_length=20)
    
    model_config = {    #Añado dentro del esquema valores por defecto en vez de hacerlo en Field()
        'json_schema_extra':{
            'example':{
                'new_user_name':'Ana',
                'new_user_lastname':'Perez',
                'new_username':'aperez'
            }
        }
    }
     

    