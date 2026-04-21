import sqlite3

class GestorBD:
    """Capa de acceso a datos para el sistema."""
    def __init__(self, db_name="sistema.db"):
        self.db_name = db_name

    def actualizar_paso_checklist(self, checklist_id, completado):
        """Marca o desmarca un paso del checklist."""
        with sqlite3.connect(self.db_name) as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                'UPDATE checklist_prospecto SET completado = ? WHERE id = ?',
                (completado, checklist_id)
            )
            conexion.commit()

    def agregar_prospecto(self, nombre, telefono, vendedor_id):
        """Inserta un nuevo prospecto en la base de datos."""
        with sqlite3.connect(self.db_name) as conexion:
            cursor = conexion.cursor()
            cursor.execute('''
                INSERT INTO prospectos (nombre, telefono, vendedor_id)
                VALUES (?, ?, ?)
            ''', (nombre, telefono, vendedor_id))
            conexion.commit()
            return cursor.lastrowid  # Devuelve el ID del prospecto recién creado
    def inicializar_checklist_prospecto(self, prospecto_id):
        """Crea los 5 pasos por defecto si el prospecto no tiene checklist."""
        pasos = [
            "Contacto inicial",
            "Medición",
            "Diseño enviado",
            "Cotización aceptada",
            "Cliente"
        ]
        with sqlite3.connect(self.db_name) as conexion:
            cursor = conexion.cursor()
            # Solo insertar si no existen ya
            cursor.execute(
                'SELECT COUNT(*) FROM checklist_prospecto WHERE prospecto_id = ?',
                (prospecto_id,)
            )
            if cursor.fetchone()[0] == 0:
                for paso in pasos:
                    cursor.execute(
                        'INSERT INTO checklist_prospecto (prospecto_id, paso_nombre, completado) VALUES (?, ?, 0)',
                        (prospecto_id, paso)
                    )
            conexion.commit()

    def marcar_como_cliente(self, prospecto_id):
        """Cuando todos los pasos están completos, actualiza es_cliente = 1."""
        with sqlite3.connect(self.db_name) as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                'UPDATE prospectos SET es_cliente = 1 WHERE id = ?',
                (prospecto_id,)
            )
            conexion.commit()

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
            # Nueva Tabla: Prospectos
            cursor.execute('''
                            CREATE TABLE IF NOT EXISTS prospectos (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                nombre TEXT NOT NULL,
                                telefono TEXT,
                                vendedor_id INTEGER,
                                es_cliente INTEGER DEFAULT 0, -- 0 = Prospecto, 1 = Cliente
                                FOREIGN KEY (vendedor_id) REFERENCES usuarios (id)
                            )
                        ''')

            # Nueva Tabla: Checklist de seguimiento
            # Aquí guardamos los pasos como: "Medición realizada", "Diseño enviado", etc.
            cursor.execute('''
                            CREATE TABLE IF NOT EXISTS checklist_prospecto (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                prospecto_id INTEGER,
                                paso_nombre TEXT,
                                completado INTEGER DEFAULT 0,
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

    def obtener_prospectos(self, usuario_id=None, es_admin=False):
        """Si es admin, trae todos. Si es vendedor, solo los suyos."""
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

    def obtener_checklist(self, prospecto_id):
        with sqlite3.connect(self.db_name) as conexion:
            cursor = conexion.cursor()
            cursor.execute('SELECT id, paso_nombre, completado FROM checklist_prospecto WHERE prospecto_id = ?',
                           (prospecto_id,))
            return cursor.fetchall()

    def validar_usuario(self, usuario, contrasena):
        """Devuelve (id, usuario, rol) si es correcto, o None."""
        with sqlite3.connect(self.db_name) as conexion:
            cursor = conexion.cursor()
            cursor.execute('''
                SELECT id, usuario, rol FROM usuarios 
                WHERE usuario = ? AND contrasena = ?
            ''', (usuario, contrasena))
            return cursor.fetchone()  # Esto devuelve una tupla, ej: (1, 'admin', 'admin')
