from ldap3 import Server, Connection, ALL, NTLM, MODIFY_ADD
from vars.conn_creds import *

# User details
new_user_name = "John"
new_user_lastname = "Doe"
new_user_cn = f"{new_user_name} {new_user_lastname}"
new_user_sam = f"{new_user_name[:1].upper()}{new_user_lastname.lower()}"
new_user_password = 'Password123!'

def launch():
    conn = connect_to_ad()
    if conn:
        create_user(conn, base_dn, new_user_cn, new_user_sam, new_user_password)
        conn.unbind()

def connect_to_ad():
    server = Server(server_name, get_info=ALL)
    conn = Connection(server, user=f'{domain_name}\\{admin_user}', password=admin_password, authentication=NTLM)
    if not conn.bind():
        print(f"Failed to connect: {conn.result}")
        return None
    return conn

def create_user(conn, base_dn, user_cn, user_sam, user_password):
    user_dn = f'CN={user_cn},{base_dn}'
    user_exists = conn.search(user_dn, '(objectClass=user)', attributes=['*'])
    if user_exists:
        print(f"User {user_cn} already exists.")
        return
    
    attributes = {
        'cn': user_cn,
        'sAMAccountName': user_sam,
        'userPrincipalName': f'{user_sam}@{domain_name}',
        'userAccountControl': 512,  # Normal account
        'givenName': 'John',
        'sn': 'Doe',
        'displayName': user_cn,
        'mail': f'{user_sam}@{domain_name}',
        'userPassword': user_password
    }

    if conn.add(user_dn, ['top', 'person', 'organizationalPerson', 'user'], attributes):
        print(f"User {user_cn} created successfully.")
        # Enable the user and set the password
        conn.extend.microsoft.modify_password(user_dn, user_password)
        conn.modify(user_dn, {'userAccountControl': [(MODIFY_ADD, [512])]})
        print("Password set and user enabled.")
    else:
        print(f"Failed to create user: {conn.result}")

def launch():
    conn = connect_to_ad()
    if conn:
        create_user(conn, base_dn, new_user_cn, new_user_sam, new_user_password)
        conn.unbind()
