from ldap3 import Server, Connection, ALL, NTLM, MODIFY_ADD, MODIFY_REPLACE
from fastapi import HTTPException
from src.vars.conn_creds import *
from src.models.ad_model import UserCreate

def create_user_attributes(user: UserCreate):
    return {
        'objectClass': ['top', 'person', 'organizationalPerson', 'user'],
        #'cn': f"{user.new_user_name} {user.new_user_middlename} {user.new_user_lastname}",
        'cn': f"{user.new_user_name} {user.new_user_lastname}",
        'sAMAccountName': f"{user.new_user_name[:1].upper()}{user.new_user_lastname.lower()}",
        'userPrincipalName': f'{user.new_user_name[:1].lower()}{user.new_user_lastname.lower()}@{domain_name}',
        'userAccountControl': 514,  # Normal account
        'givenName': user.new_user_name,
        'sn': user.new_user_lastname,
        #'displayName': f"{user.new_user_name} {user.new_user_middlename} {user.new_user_lastname}",
        'displayName': f"{user.new_user_name} {user.new_user_lastname}",
        'mail': f'{user.new_username.lower()}@{domain_name}',
    #    'userPassword': user.new_user_password
    }


