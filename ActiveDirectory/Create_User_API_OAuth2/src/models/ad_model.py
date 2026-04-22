from pydantic import BaseModel, Field

  
class UserCreate(BaseModel):
    new_user_name: str = Field(min_length=3, max_length=50) #Optional[int] = None o se puede declarar id: int | None = None
    new_user_lastname: str = Field(min_length=3, max_length=30) #Optional[str] = None o se puede declarar new_user_password: str | None = None
    new_username: str = Field(min_length=3, max_length=30)
    
    model_config = {    #Añado dentro del esquema valores por defecto en vez de hacerlo en Field()
        'json_schema_extra':{
            'example':{
                'new_user_name':'Ana',
                'new_user_lastname':'Perez',
                'new_username':'aperez'
            }
        }
    }
     
class UserPasswordChange(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    new_user_password: str = Field(min_length=8, max_length=128)
        
    model_config = {    #Añado dentro del esquema valores por defecto en vez de hacerlo en Field()
        'json_schema_extra':{
            'example':{
                'username':'aperez',
                'new_user_password':'P@ssw0rd123'
            }
        }
    }