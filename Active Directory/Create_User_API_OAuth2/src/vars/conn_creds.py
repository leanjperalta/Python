import os

server_name = 'ldap://hpg-ad.garrahan.gov.ar'
domain_name = 'garrahan.gov.ar'
admin_user = 'lperalta'
admin_password = os.environ.get('LP_PASS')
base_dn = 'OU=Test,DC=garrahan,DC=gov,DC=ar'