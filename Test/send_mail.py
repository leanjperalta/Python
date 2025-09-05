#Tiny script for testing 365 smtp over STARTTLS

import smtplib
import os
from email.mime.text import MIMEText
 
msg = MIMEText("Este es el cuerpo del mensaje")
msg["Subject"] = "Asunto de prueba"
msg["From"] = "xxx@domain.com"
msg["To"] = "lperalta@domain.com"
 
smtp_server = "smtp.office365.com"
smtp_port = 587
user = "xxx@domain.com"
password = os.environ.get('EMAIL_PASS') #1st create local env var
 
with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.starttls()
    server.login(user, password)
    server.send_message(msg)
