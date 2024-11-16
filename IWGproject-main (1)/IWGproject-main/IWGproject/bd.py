import sqlite3

# Crear la conexión a la base de datos (esto creará el archivo database.sqlite3 si no existe)
conn = sqlite3.connect('database.sqlite3')

# Crear un cursor para interactuar con la base de datos
cursor = conn.cursor()

# Crear la tabla 'usuarios'
cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    rut TEXT NOT NULL UNIQUE,
    medio_transporte TEXT NOT NULL
)
''')

# Crear la tabla 'kilometros_recorridos'
cursor.execute('''
CREATE TABLE IF NOT EXISTS kilometros_recorridos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    fecha TEXT NOT NULL,
    kilometros REAL NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
)
''')

# Guardar los cambios y cerrar la conexión
conn.commit()
conn.close()