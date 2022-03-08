from tkinter import font
import mysql.connector
from tkinter import *
from tkinter import ttk
from mysql import *
from tkinter.messagebox import *
# CREA LA BASE DE DATOS

mibase = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd=""
)
crear_base = mibase.cursor()

crear_base.execute("create database if not exists tp_final")


conexion1 = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="tp_final"
)

micursor = conexion1.cursor()

micursor.execute("create table if not exists trabajo_final( id int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT, nombre VARCHAR(128) COLLATE utf8_spanish2_ci NOT NULL, apellido varchar(128) COLLATE utf8_spanish2_ci NOT NULL, dni int(8) UNIQUE COLLATE utf8_spanish2_ci NOT NULL )")


# VARIABLES GLOBALES


id = 0
########FUNCIONES################


def alta():
    global id
    id += 1
    tree.insert(
        "", "end", text=str(id), values=(nombre.get(), apellido.get(), dni.get())
    )
    sql = "INSERT INTO trabajo_final (nombre, apellido, dni) VALUES (%s, %s, %s)"
    datos = (nombre.get(), apellido.get(), dni.get())

    micursor.execute(sql, datos)

    conexion1.commit()

    print(micursor.rowcount, "Cantidad de registros agregados.")
    showinfo(title="Alta",
             message="La base de datos ha sido actualizada con éxito")


def reg_print():

    micursor.execute("select id, nombre, apellido, dni from trabajo_final")
    for fila in micursor:
        print(fila)
    showinfo(title="Base actualizada",
             message="Por favor verifique los datos en su consola")


def borrar_registro():
    cursor1 = conexion1.cursor()
    cursor1.execute("DELETE from trabajo_final where id=" + id1.get())
    conexion1.commit()
    showinfo(title="Registro borrado",
             message="La operación ha sido realizada con éxito")


def modificar():
    nom = nombre.get()
    app = apellido.get()
    doc = dni.get()
    aid = id1.get()

    cursor1 = conexion1.cursor()
    sql = f"UPDATE trabajo_final SET nombre = '{nom}', apellido= '{app}', dni='{doc}' WHERE id='{aid}'"
    cursor1.execute(sql)
    conexion1.commit()

    showinfo(title="Base modificada",
             message="La base de datos ha sido modificada")


"""
TKINTER
"""


ventana = Tk()

ventana.geometry("500x500")
ventana.title("UNIVERSIDAD DE BUENOS AIRES")
label = Label(ventana, text='Ingrese sus datos: ', font=(12))
label.pack(anchor=CENTER)
label.config(bg='lightgreen', width=400)

l_nombre = Label(ventana, text="Nombre", font=(10)).place(x=0, y=45)
l_apellido = Label(ventana, text="Apellido", font=(10)).place(x=0, y=90)
l_dni = Label(ventana, text="DNI", font=(10)).place(x=0, y=135)
l_id = Label(ventana, text="ID", font=(10)).place(x=250, y=45)

id1 = Entry(ventana)
nombre = Entry(ventana)
apellido = Entry(ventana)
dni = Entry(ventana)

id1.place(x=300, y=45)
nombre.place(x=100, y=45)
apellido.place(x=100, y=90)
dni.place(x=100, y=135)

# BOTONES

boton_alta = Button(ventana, text="Alta", command=alta, padx=10,
                    pady=3, activebackground="green", activeforeground="white")
boton_alta.place(x=40, y=200)

boton_imprimir_reg = Button(ventana, text="Imprimir registro",
                            command=reg_print, padx=10, pady=3)
boton_imprimir_reg.place(x=175, y=200)

boton_borrar_reg = Button(ventana, text="Borrar registro",
                          command=borrar_registro, padx=10, pady=3)
boton_borrar_reg.place(x=305, y=70)

boton_modificar = Button(ventana, text="Modificar",
                         command=modificar, padx=10, pady=3)
boton_modificar.place(x=350, y=200)

####Treeview#####

tree = ttk.Treeview(ventana)
tree["columns"] = ("col1", "col2", "col3")
tree.column("#0", width=80, minwidth=80, anchor=W)
tree.column("col1", width=110, minwidth=110)
tree.column("col2", width=110, minwidth=110)
tree.column("col3", width=130, minwidth=130)

tree.heading("#0", text="ID")
tree.heading("col1", text="Nombre")
tree.heading("col2", text="Apellido")
tree.heading("col3", text="DNI")
tree.place(x=40, y=250)

# Impresión de base

micursor.execute("select id, nombre, apellido, dni from trabajo_final")
for fila in micursor:
    print(fila)

mainloop()
