import sqlite3
import json


class GestorBD:
    """Capa de acceso a datos para el sistema."""

    def __init__(self, db_name="sistema.db"):
        self.db_name = db_name

    def inicializar_bd(self):
        with sqlite3.connect(self.db_name) as conexion:
            cursor = conexion.cursor()

            # Tabla Usuarios
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario TEXT UNIQUE NOT NULL,
                    contrasena TEXT NOT NULL,
                    rol TEXT NOT NULL
                )
            ''')

            # Tabla Prospectos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS prospectos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    telefono TEXT,
                    vendedor_id INTEGER,
                    es_cliente INTEGER DEFAULT 0,
                    FOREIGN KEY (vendedor_id) REFERENCES usuarios (id)
                )
            ''')

            # Tabla Citas (Fase 1)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS citas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    prospecto_id INTEGER,
                    fecha TEXT NOT NULL,
                    hora TEXT NOT NULL,
                    FOREIGN KEY (prospecto_id) REFERENCES prospectos (id)
                )
            ''')

            # NUEVA TABLA: Formulario de Medición (Fase 2)
            # Agrupamos los datos principales en columnas y los detalles técnicos en JSON
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS formulario_medicion (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    prospecto_id INTEGER UNIQUE,

                    -- Datos Generales
                    fecha_visita TEXT,
                    pago_visita TEXT,
                    importe_visita TEXT,
                    importe_3d TEXT,
                    fraccionamiento TEXT,
                    prototipo TEXT,
                    vive_ahi TEXT,
                    direccion TEXT,
                    como_entero TEXT,
                    cuando_compra TEXT,

                    -- Secciones empaquetadas en JSON para flexibilidad
                    presupuesto_json TEXT,
                    distribucion_json TEXT,
                    acabados_json TEXT,
                    equipos_json TEXT,

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

    # --- MÉTODOS DE PROSPECTOS ---
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

    # --- MÉTODOS DE CITAS (FASE 1) ---
    def agendar_cita(self, prospecto_id, fecha, hora):
        with sqlite3.connect(self.db_name) as conexion:
            cursor = conexion.cursor()
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
        with sqlite3.connect(self.db_name) as conexion:
            cursor = conexion.cursor()
            cursor.execute('SELECT fecha, hora FROM citas WHERE prospecto_id = ?', (prospecto_id,))
            return cursor.fetchone()

    # --- NUEVOS MÉTODOS: MEDICIÓN (FASE 2) ---
    def guardar_medicion(self, prospecto_id, datos_generales, presupuesto, distribucion, acabados, equipos):
        """
        Guarda o actualiza el cuestionario de medición.
        Los parámetros presupuesto, distribucion, acabados y equipos son diccionarios (dict) de Python.
        """
        with sqlite3.connect(self.db_name) as conexion:
            cursor = conexion.cursor()

            # Convertimos los diccionarios a strings JSON
            presupuesto_str = json.dumps(presupuesto)
            distribucion_str = json.dumps(distribucion)
            acabados_str = json.dumps(acabados)
            equipos_str = json.dumps(equipos)

            cursor.execute('SELECT id FROM formulario_medicion WHERE prospecto_id = ?', (prospecto_id,))
            existe = cursor.fetchone()

            if existe:
                cursor.execute('''
                    UPDATE formulario_medicion 
                    SET fecha_visita=?, pago_visita=?, importe_visita=?, importe_3d=?, 
                        fraccionamiento=?, prototipo=?, vive_ahi=?, direccion=?, como_entero=?, cuando_compra=?,
                        presupuesto_json=?, distribucion_json=?, acabados_json=?, equipos_json=?
                    WHERE prospecto_id=?
                ''', (*datos_generales, presupuesto_str, distribucion_str, acabados_str, equipos_str, prospecto_id))
            else:
                cursor.execute('''
                    INSERT INTO formulario_medicion (
                        prospecto_id, fecha_visita, pago_visita, importe_visita, importe_3d,
                        fraccionamiento, prototipo, vive_ahi, direccion, como_entero, cuando_compra,
                        presupuesto_json, distribucion_json, acabados_json, equipos_json
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (prospecto_id, *datos_generales, presupuesto_str, distribucion_str, acabados_str, equipos_str))
            conexion.commit()

    def obtener_medicion(self, prospecto_id):
        """Devuelve todos los datos de la medición si existen, o None."""
        with sqlite3.connect(self.db_name) as conexion:
            cursor = conexion.cursor()
            cursor.execute('''
                SELECT fecha_visita, pago_visita, importe_visita, importe_3d,
                       fraccionamiento, prototipo, vive_ahi, direccion, como_entero, cuando_compra,
                       presupuesto_json, distribucion_json, acabados_json, equipos_json
                FROM formulario_medicion WHERE prospecto_id = ?
            ''', (prospecto_id,))
            resultado = cursor.fetchone()

            if resultado:
                # Convertimos los JSON de vuelta a diccionarios de Python
                datos = list(resultado[:10])
                datos.append(json.loads(resultado[10]) if resultado[10] else {})
                datos.append(json.loads(resultado[11]) if resultado[11] else {})
                datos.append(json.loads(resultado[12]) if resultado[12] else {})
                datos.append(json.loads(resultado[13]) if resultado[13] else {})
                return datos
            return None

    def validar_usuario(self, usuario, contrasena):
        with sqlite3.connect(self.db_name) as conexion:
            cursor = conexion.cursor()
            cursor.execute('SELECT id, usuario, rol FROM usuarios WHERE usuario = ? AND contrasena = ?',
                           (usuario, contrasena))
            return cursor.fetchone()