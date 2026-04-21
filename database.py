import sqlite3


class GestorBD:
    """Capa de acceso a datos para el sistema."""

    def __init__(self, db_name="sistema.db"):
        self.db_name = db_name

    def inicializar_bd(self):
        """Crea las tablas iniciales y usuarios por defecto."""
        with sqlite3.connect(self.db_name) as conexion:
            cursor = conexion.cursor()

            # Tabla de Usuarios
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario TEXT UNIQUE NOT NULL,
                    contrasena TEXT NOT NULL,
                    rol TEXT NOT NULL
                )
            ''')

            # Tabla de Prospectos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS prospectos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    telefono TEXT NOT NULL,
                    vendedor_id INTEGER,
                    es_cliente INTEGER DEFAULT 0,
                    FOREIGN KEY (vendedor_id) REFERENCES usuarios (id)
                )
            ''')

            # NUEVA TABLA: Citas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS citas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    prospecto_id INTEGER,
                    fecha TEXT NOT NULL,
                    hora TEXT NOT NULL,
                    FOREIGN KEY (prospecto_id) REFERENCES prospectos (id)
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

    def agregar_prospecto(self, nombre, telefono, vendedor_id):
        with sqlite3.connect(self.db_name) as conexion:
            cursor = conexion.cursor()
            cursor.execute('''
                INSERT INTO prospectos (nombre, telefono, vendedor_id)
                VALUES (?, ?, ?)
            ''', (nombre, telefono, vendedor_id))
            conexion.commit()
            return cursor.lastrowid

    def obtener_prospectos(self, usuario_id=None, es_admin=False):
        with sqlite3.connect(self.db_name) as conexion:
            cursor = conexion.cursor()
            if es_admin:
                cursor.execute('''
                    SELECT p.id, p.nombre, p.telefono, u.usuario, p.es_cliente 
                    FROM prospectos p 
                    JOIN usuarios u ON p.vendedor_id = u.id
                ''')
            else:
                cursor.execute('SELECT id, nombre, telefono, es_cliente FROM prospectos WHERE vendedor_id = ?',
                               (usuario_id,))
            return cursor.fetchall()

    # --- NUEVOS MÉTODOS PARA CITAS ---
    def agendar_cita(self, prospecto_id, fecha, hora):
        """Guarda o actualiza la cita del prospecto."""
        with sqlite3.connect(self.db_name) as conexion:
            cursor = conexion.cursor()
            # Verificamos si ya tiene una cita para actualizarla
            cursor.execute('SELECT id FROM citas WHERE prospecto_id = ?', (prospecto_id,))
            cita_existente = cursor.fetchone()

            if cita_existente:
                cursor.execute('UPDATE citas SET fecha = ?, hora = ? WHERE prospecto_id = ?',
                               (fecha, hora, prospecto_id))
            else:
                cursor.execute('INSERT INTO citas (prospecto_id, fecha, hora) VALUES (?, ?, ?)',
                               (prospecto_id, fecha, hora))
            conexion.commit()

    def obtener_cita(self, prospecto_id):
        """Devuelve (fecha, hora) si existe, o None."""
        with sqlite3.connect(self.db_name) as conexion:
            cursor = conexion.cursor()
            cursor.execute('SELECT fecha, hora FROM citas WHERE prospecto_id = ?', (prospecto_id,))
            return cursor.fetchone()

    def validar_usuario(self, usuario, contrasena):
        with sqlite3.connect(self.db_name) as conexion:
            cursor = conexion.cursor()
            cursor.execute('SELECT id, usuario, rol FROM usuarios WHERE usuario = ? AND contrasena = ?',
                           (usuario, contrasena))
            return cursor.fetchone()