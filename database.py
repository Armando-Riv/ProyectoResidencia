import sqlite3

class GestorBD:
    """Capa de acceso a datos para el sistema."""
    def __init__(self, db_name="sistema.db"):
        self.db_name = db_name

    def inicializar_bd(self):
        """Crea las tablas iniciales y usuarios por defecto."""
        with sqlite3.connect(self.db_name) as conexion:
            cursor = conexion.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario TEXT UNIQUE NOT NULL,
                    contrasena TEXT NOT NULL,
                    rol TEXT NOT NULL
                )
            ''')
            usuarios_prueba = [
                ('admin', 'admin123', 'admin'),
                ('vendedor1', 'ventas123', 'vendedor')
            ]
            cursor.executemany('''
                INSERT OR IGNORE INTO usuarios (usuario, contrasena, rol) 
                VALUES (?, ?, ?)
            ''', usuarios_prueba)
            conexion.commit()

    def validar_usuario(self, usuario, contrasena):
        """Devuelve el rol del usuario si las credenciales son correctas, o None."""
        with sqlite3.connect(self.db_name) as conexion:
            cursor = conexion.cursor()
            cursor.execute('''
                SELECT rol FROM usuarios 
                WHERE usuario = ? AND contrasena = ?
            ''', (usuario, contrasena))
            resultado = cursor.fetchone()
            return resultado[0] if resultado else None