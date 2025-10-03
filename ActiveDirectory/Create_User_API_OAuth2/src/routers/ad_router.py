from .auth import oauth2_scheme, login
from fastapi.security import OAuth2PasswordRequestForm  # Add this import
from fastapi import APIRouter, HTTPException, Depends
from ..models.ad_model import UserCreate #llamada al modelo UserCreate
from ldap3 import Server, Connection, ALL, NTLM, MODIFY_ADD
from ..vars.conn_creds import *
import string, random


aduser_router = APIRouter() #este router va a contener la ruta para crear un usuario

@aduser_router.post("/token")
async def token(form_data: OAuth2PasswordRequestForm = Depends()):
    return await login(form_data)

@aduser_router.post("/create_user")
def create_user(user: UserCreate, token: str = Depends(oauth2_scheme)):
    try:
        server = Server(server_name, get_info=ALL)
        conn = Connection(server, user=f'{domain_name}\\{admin_user}', password=admin_password, authentication=NTLM)
        
        if not conn.bind():
            raise Exception(f"Failed to bind to LDAP server: {conn.result}")

        #seteo canonical name (no lo uso como atributo)
        cn_user=f"{user.new_user_name} {user.new_user_lastname}"
        #seteo sAMAccountname
        #sam_user=f"{user.new_user_name[:1].lower()}{user.new_user_lastname.lower()}"
        sam_user=f"{user.new_username}"
        #seteo UserPrincipalName
        #pn_user=f"{user.new_user_name[:1].lower()}{user.new_user_lastname.lower()}@{domain_name}"
        pn_user=f"{user.new_username}@{domain_name}"
        #seteo casilla del usuario
        #mail_user=f"{user.new_user_name[:1].lower()}{user.new_user_lastname.lower()}@{domain_name}"
        mail_user=f"{user.new_username}@{domain_name}"
        display_name=f"{user.new_user_name} {user.new_user_lastname}"
        #seteo distinguished name
        dn = f"CN={cn_user},{base_dn}"

        user_exists = conn.search(dn, '(objectClass=user)', attributes=['*']) ## Validacion borrar
        if user_exists:
            raise HTTPException(status_code=500, detail=f"LDAP error: El objeto ya existe")
        

        
        #genero un password random de 8 char (letras, numeros y puntuación)
        password_length = 8
        password_characters = string.ascii_letters + string.digits + string.punctuation
        userpassword = ''.join(random.choice(password_characters) for _ in range(password_length))
        enc_pwd = '"{}"'.format(userpassword).encode('utf-16-le')

        #creo los atributos del usuario
        attrs = {
            'objectClass': ['User', 'posixAccount', 'top'],
            #'cn': cn_user,
            'sn': user.new_user_lastname,
            'sAMAccountName': sam_user,
            'givenName': user.new_user_name,
            #'uid': user.username,
            'userPrincipalName': pn_user,
            'mail': mail_user,
            'displayName': display_name,
        }
     
        if not conn.add(dn, attributes=attrs):
            raise HTTPException(status_code=404, detail=f"Failed to add user: {conn.result}")
        
        conn.extend.microsoft.modify_password(dn, enc_pwd)
        conn.modify(dn, {'userAccountControl': [('MODIFY_REPLACE', 512)]})

        # Add user to Domain Users group - skip if already exists
        domain_users_dn = f"CN=Domain Users,CN=Users,{','.join(base_dn.split(',')[1:])}"
        try:
            conn.extend.microsoft.add_members_to_groups(dn, domain_users_dn)
        except Exception as e:
            if "entryAlreadyExists" not in str(e):  # ignore if already member
                raise HTTPException(status_code=500, detail=f"Failed to add user to Domain Users: {str(e)}")
            
        # Add user to Internet-General group
        domain_group_dn = f"CN=Internet-General,{','.join(base_dn.split(',')[1:])}"
        try:
            success = conn.extend.microsoft.add_members_to_groups(dn, domain_group_dn)
            if not success:
                raise HTTPException(status_code=500, detail=f"Failed to add user to Internet-General: {conn.result}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error adding to Internet-General: {str(e)}")

        # Desconecto del servidor
        conn.unbind()

        return {"message": f"Usuaria/o {user.new_user_name} {user.new_user_lastname} creada/o satisfactoriamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LDAP error: {str(e)}")
