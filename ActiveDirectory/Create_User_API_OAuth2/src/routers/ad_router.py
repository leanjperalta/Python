from .auth import oauth2_scheme, login
from fastapi.security import OAuth2PasswordRequestForm  # Add this import
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from ..models.ad_model import UserCreate #llamada al modelo UserCreate
from ldap3 import Server, Connection, ALL, NTLM, MODIFY_ADD
from ldap3.utils.conv import escape_filter_chars
from ..vars.conn_creds import *
from ..ad.usercreate import create_user_attributes
from pydantic import BaseModel
import string, random


aduser_router = APIRouter() #este router va a contener la ruta para crear un usuario

class CreateUserResponse(BaseModel):
    status: str
    message: str

@aduser_router.post("/token")
async def token(form_data: OAuth2PasswordRequestForm = Depends()):
    return await login(form_data)

@aduser_router.post("/create_user", status_code=201, response_model=CreateUserResponse)
def create_user(user: UserCreate, token: str = Depends(oauth2_scheme)):
    try:
        server = Server(server_name, get_info=ALL)
        conn = Connection(server, user=f'{domain_name}\\{admin_user}', password=admin_password, authentication=NTLM)
        
        if not conn.bind():
            raise Exception(f"Falló conexión a servidor LDAP: {conn.result}")

        #verifico si el usuario ya existe buscando por cn con caracteres escapados
        cn_value = f"{user.new_user_name} {user.new_user_lastname}"
        escaped_cn = escape_filter_chars(cn_value)
        filter_str = f"(&(objectClass=user)(cn={escaped_cn}))"
        
        conn.search(root_dn, filter_str, attributes=['*'])
        if conn.entries:
        #    return JSONResponse(status_code=500, content={"status": "error", "message": "LDAP error: El usuario ya existe"})
            cn_value = f"{cn_value} {user.new_username}"

        #creo los atributos del usuario
        attrs = create_user_attributes(user, cn_value)

        # Intentar agregar usuario
      
        #seteo distinguished name
        dn = f"CN={cn_value},{base_dn}"
      
        try:
            add_result = conn.add(dn, attributes=attrs)
            if not add_result:
                raise HTTPException(status_code=404, detail=f"Error al agregar usuario: {conn.result}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en conn.add(): {str(e)} - {conn.result}")
        
        #genero un password random de 8 char (letras, numeros y puntuación)
        password_length = 8
        password_characters = string.ascii_letters + string.digits + string.punctuation
        userpassword = ''.join(random.choice(password_characters) for _ in range(password_length))
        enc_pwd = '"{}"'.format(userpassword).encode('utf-16-le')

        try:
            conn.extend.microsoft.modify_password(dn, enc_pwd)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al establecer contraseña: {str(e)}")
        
        try:
            conn.modify(dn, {'userAccountControl': [('MODIFY_REPLACE', 512)]})
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al activar usuario: {str(e)}")

        # Agrego usuario al grupo Domain Users
        domain_users_dn = f"CN=Domain Users,CN=Users,{','.join(base_dn.split(',')[1:])}"
        try:
            conn.extend.microsoft.add_members_to_groups(dn, domain_users_dn)
        except Exception as e:
            if "entryAlreadyExists" not in str(e):  # ignorar si el usuario ya es miembro del grupo
                raise HTTPException(status_code=500, detail=f"Error agregando usuario al grupo Domain Users: {str(e)}")
            
        # Agrego usuario al grupo Internet-General
        domain_group_dn = f"CN=Internet-General,{','.join(base_dn.split(',')[1:])}"
        try:
            success = conn.extend.microsoft.add_members_to_groups(dn, domain_group_dn)
            if not success:
                raise HTTPException(status_code=500, detail=f"Error añadiendo usuario al grupo Internet-General: {conn.result}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error añadiendo pertenencia a Internet-General: {str(e)}")

        # Desconecto del servidor
        conn.unbind()

        return {"status": "success",  "message": f"Usuaria/o {user.new_user_name} {user.new_user_lastname} creada/o satisfactoriamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
