from ldap3 import Server, Connection, ALL, NTLM, MODIFY_ADD, MODIFY_REPLACE
from fastapi import HTTPException
from src.vars.conn_creds import *
from src.models.ad_model import UserCreate

def create_user(user: UserCreate):
    server = Server(server_name, get_info=ALL)
    conn = Connection(server, user=f'{domain_name}\\{admin_user}', password=admin_password, authentication=NTLM)
    if not conn.bind():
        raise HTTPException(status_code=500, detail="Failed to connect to Active Directory")
#    return conn
#    user_dn = f'CN={user_cn},{base_dn}'
#    user_exists = conn.search(user_dn, '(objectClass=user)', attributes=['*'])
#    if user_exists:
#        print(f"User {user_cn} already exists.")
#        return
    
    attributes = {
        'objectClass': ['top', 'person', 'organizationalPerson', 'user'],
        'cn': f"{user.new_user_name} {user.new_user_middlename} {user.new_user_lastname}",
        'sAMAccountName': f"{user.new_user_name[:1].upper()}{user.new_user_lastname.lower()}",
        'userPrincipalName': f'{user_sam}@{domain_name}',
        'userAccountControl': 514,  # Normal account
        'givenName': user.new_user_name,
        'sn': user.new_user_lastname,
        'displayName': f"{user.new_user_name} {user.new_user_middlename} {user.new_user_lastname}",
        'mail': f'{user_sam}@{domain_name}',
        'userPassword': user.new_user_password
    }

    if conn.add(base_dn, attributes):
        print(f"User {user.new_user_name} {user.new_user_middlename} {user.new_user_lastname} created successfully.")
        # Enable the user and set the password
    #    conn.extend.microsoft.modify_password(user_dn, user_password)
    #    conn.modify(user_dn, {'userAccountControl': [(MODIFY_REPLACE, [514])]}) # 514 = User set to disabled
    else:
        raise Exception(f"Failed to create user: {conn.result}")

    return

