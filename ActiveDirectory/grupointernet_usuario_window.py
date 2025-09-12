#UI para consulta de pertenencia de grupo de usuario de dominio

from ldap3 import Server, Connection, NTLM
from tkinter import *

#DC Server
server = Server("domain") 

window = Tk()

def consulta():

    flag = 0
    
    try:
        with Connection(server, user="{}\\{}".format("domain", "user"), password="password", authentication=NTLM) as conn:
            conn.search("dc=xxxx,dc=xxxx,dc=xxxxx", "(&(sAMAccountName={}))".format(entry_value.get()),
                    attributes=['memberOf'])
            entry = conn.entries
        
            for group in entry[0]['memberOf']:
                if group.startswith('CN=Internet'):
                    txt.delete(1.0,END)
                    txt.insert(END,group)
                    flag = 1
            
            if flag == 0:
                txt.delete(1.0,END)
                txt.insert(END,"No posee acceso a Internet")
    
    except IndexError: #Si user no existe
         txt.delete(1.0,END)
         txt.insert(END,"No existe el usuario")

def entry_delete():
     entry.delete(0,END)

window.title("Consulta Membresía Internet - AD")
window.geometry('400x80+10+10')
# Root Window Label
lbl = Label(window, text = "Ingrese Usuario")
lbl.grid(row=0, column=0, sticky=W, pady=2)
# Entry Field
entry_value = StringVar()
entry = Entry(window, textvariable=entry_value)
entry.grid(row =0, column= 1, sticky=W, pady=2)
# Button Widget
boton1 = Button(window,text='Consultar',command=consulta)
boton1.grid(row=0,column=2)
# Text Grid
txt = Text(window,height=1,width=49)
txt.place(x=0,y=35)
boton2 = Button(window,bg='red',text='X',command=entry_delete)
boton2.grid(row=0,column=4)

window.mainloop()
