from fastapi.responses import JSONResponse
from fastapi import Path, Query, APIRouter, HTTPException
from ..models.ad_model import UserCreate #llamada al modelo UserCreate
from ldap3 import Server, Connection, ALL, NTLM, MODIFY_ADD
from ..vars.conn_creds import *

aduser_router = APIRouter() #este router va a contener la ruta para crear un usuario

@aduser_router.post("/create_user")
def create_user(user: UserCreate):
    try:
        server = Server(server_name, get_info=ALL)

        conn = Connection(server, user=f'{domain_name}\\{admin_user}', password=admin_password, authentication=NTLM)
        
        
        if not conn.bind():
            raise Exception(f"Failed to bind to LDAP server: {conn.result}")

        cn_user=f"{user.new_user_name} {user.new_user_lastname}"
        sam_user=f"{user.new_user_name[:1].lower()}{user.new_user_lastname.lower()}"
        pn_user=f"{user.new_user_name[:1].lower()}{user.new_user_lastname.lower()}@{domain_name}"
        mail_user=f"{user.new_user_name[:1].lower()}{user.new_user_lastname.lower()}@{domain_name}"

        dn = f"CN={cn_user},{base_dn}"
        #creo los atributos del usuario
        userpassword = 'garra123'
        enc_pwd = '"{}"'.format(userpassword).encode('utf-16-le')

        attrs = {
            'objectClass': ['User', 'posixAccount', 'top'],
            #'cn': cn_user,
            'sn': user.new_user_lastname,
            'sAMAccountName': sam_user,
            'givenName': user.new_user_name,
            #'uid': user.username,
            'userPrincipalName': pn_user,
            'mail': mail_user,
        }
     
        if not conn.add(dn, attributes=attrs):
            raise HTTPException(status_code=404, detail=f"Failed to add user: {conn.result}")
        
        conn.extend.microsoft.modify_password(dn, enc_pwd)
        conn.modify(dn, {'userAccountControl': [('MODIFY_REPLACE', 512)]})

        domain_users_dn = f"CN=Domain Users,CN=Users,{','.join(base_dn.split(',')[1:])}"
        domain_group_dn = f"CN=Internet-General,{','.join(base_dn.split(',')[1:])}"
        conn.extend.microsoft.add_members_to_groups(dn, domain_users_dn)
        conn.extend.microsoft.add_members_to_groups(dn, domain_group_dn)

        # Desconecto del servidor
        conn.unbind()

        return {"message": f"User {user.new_user_name} created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LDAP error: {str(e)}")


