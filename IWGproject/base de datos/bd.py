import sqlite3

#esto es para conectarse a la base de datos
conectar = sqlite3.connect("proyecto.db")
#esto es para crear tablas u otros
c = conectar.cursor()

#c.execute("""CREATE TABLE usuarios (
#            nombre TEXT,
#            carrera TEXT,
#            edad REAL
#)""")
usuarios = []
c.executemany("INSERT INTO estudiantes VALUES (?,?,?),nombre_archivo_datos")
conectar.commit()
conectar.close()