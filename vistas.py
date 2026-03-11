import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                               QPushButton, QFrame, QMessageBox, QGraphicsDropShadowEffect)
from PySide6.QtGui import QPixmap, QIcon, QAction
from PySide6.QtCore import Qt, QSize
from database import GestorBD


# --- CLASE PADRE (HERENCIA) ---
class VentanaBase(QWidget):
    """Clase base que contiene el comportamiento común de las ventanas."""

    def __init__(self, titulo, ancho, alto):
        super().__init__()
        self.setWindowTitle(titulo)
        self.setFixedSize(ancho, alto)
        self.setWindowFlag(Qt.WindowType.WindowMaximizeButtonHint, False)

    def centrar_ventana(self):
        """Centra la ventana en el monitor actual."""
        geometria = self.frameGeometry()
        centro = self.screen().availableGeometry().center()
        geometria.moveCenter(centro)
        self.move(geometria.topLeft())

    def cerrar_sesion(self):
        """Cierra la ventana actual y regresa al Login."""
        self.ventana_login = VentanaLogin()
        self.ventana_login.show()
        self.close()


# --- PANTALLAS HIJAS ---
class VentanaAdmin(VentanaBase):
    def __init__(self):
        super().__init__("Panel Administrativo - Excellence Cocinas", 560, 460)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        titulo = QLabel("Panel Administrativo")
        titulo.setStyleSheet("font-size: 20px; font-weight: bold; color: #2C3E50; margin-bottom: 20px;")

        descripcion = QLabel("Gestión de inventario de muebles y materiales.")
        descripcion.setStyleSheet("font-size: 14px; color: #555;")

        self.boton_logout = QPushButton("Cerrar Sesión")
        self.boton_logout.setFixedSize(150, 40)
        self.boton_logout.setStyleSheet(
            "background-color: #E74C3C; color: white; border-radius: 5px; font-weight: bold; margin-top: 30px;")
        self.boton_logout.clicked.connect(self.cerrar_sesion)

        layout.addWidget(titulo, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(descripcion, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.boton_logout, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)
        self.centrar_ventana()


class VentanaVendedor(VentanaBase):
    def __init__(self):
        super().__init__("Módulo de Ventas - Excellence Cocinas", 500, 400)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        titulo = QLabel("Panel de Ventas")
        titulo.setStyleSheet("font-size: 20px; font-weight: bold; color: #27AE60; margin-bottom: 20px;")

        descripcion = QLabel("Cotizaciones y catálogo.")
        descripcion.setStyleSheet("font-size: 14px; color: #555;")

        self.boton_logout = QPushButton("Cerrar Sesión")
        self.boton_logout.setFixedSize(150, 40)
        self.boton_logout.setStyleSheet(
            "background-color: #E74C3C; color: white; border-radius: 5px; font-weight: bold; margin-top: 30px;")
        self.boton_logout.clicked.connect(self.cerrar_sesion)

        layout.addWidget(titulo, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(descripcion, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.boton_logout, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)
        self.centrar_ventana()


from PySide6.QtGui import QAction # <--- ¡Asegúrate de agregar QAction a tus importaciones de QtGui arriba!

# --- INTERFAZ DE LOGIN ---
class VentanaLogin(VentanaBase):
    def __init__(self):
        super().__init__("Excellence Cocinas - Acceso", 500, 560)
        self.setStyleSheet("background-color: #2C3E50;")

        layout_principal = QVBoxLayout()
        layout_principal.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.card = QFrame()
        self.card.setFixedSize(380, 500)
        self.card.setStyleSheet("QFrame { background-color: white; border-radius: 12px; }")

        layout_card = QVBoxLayout(self.card)
        layout_card.setContentsMargins(35, 30, 35, 30)
        layout_card.setSpacing(10)

        # --- Logo ---
        self.label_logo = QLabel()
        logo_path = os.path.join(os.path.dirname(__file__), 'logo_excellence.png')
        pixmap_logo = QPixmap(logo_path)

        if not pixmap_logo.isNull():
            self.label_logo.setPixmap(pixmap_logo.scaledToWidth(250, Qt.TransformationMode.SmoothTransformation))
            self.label_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.label_logo.setStyleSheet("background-color: transparent; margin-bottom: 25px; margin-top: 10px;")
            layout_card.addWidget(self.label_logo)
        else:
            self.label_titulo = QLabel("Excellence Cocinas")
            self.label_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.label_titulo.setStyleSheet(
                "background-color: transparent; font-size: 22px; font-weight: bold; color: #FF6B00; margin-bottom: 25px;")
            layout_card.addWidget(self.label_titulo)

        # --- Estilos base ---
        estilo_input = """
            QLineEdit { 
                background-color: #FDFDFD; 
                border: 1px solid #E5E9EC; 
                border-radius: 6px; 
                padding: 10px 12px; 
                font-size: 14px; 
                color: #333; 
            }
            QLineEdit:focus { border: 1px solid #FF6B00; }
        """
        estilo_label = "background-color: transparent; font-weight: bold; color: #666; font-size: 14px; margin-top: 10px;"

        # --- Campo: Usuario ---
        self.label_usuario = QLabel("Usuario")
        self.label_usuario.setStyleSheet(estilo_label)
        self.input_usuario = QLineEdit()
        self.input_usuario.setPlaceholderText("Ingresa tu usuario")
        self.input_usuario.setStyleSheet(estilo_input)
        layout_card.addWidget(self.label_usuario)
        layout_card.addWidget(self.input_usuario)

        # --- Campo: Contraseña con Ícono Nativo Integrado ---
        self.label_contrasena = QLabel("Contraseña")
        self.label_contrasena.setStyleSheet(estilo_label)
        layout_card.addWidget(self.label_contrasena)

        self.input_contrasena = QLineEdit()
        self.input_contrasena.setPlaceholderText("Ingresa tu contraseña")
        self.input_contrasena.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_contrasena.setStyleSheet(estilo_input)

        # Usamos QAction para poner el ícono DENTRO del campo de texto
        ruta_icono_ver = os.path.join(os.path.dirname(__file__), 'ver.png')
        self.accion_ver_pass = self.input_contrasena.addAction(QIcon(ruta_icono_ver), QLineEdit.ActionPosition.TrailingPosition)
        self.accion_ver_pass.triggered.connect(self.alternar_contrasena)

        layout_card.addWidget(self.input_contrasena)

        # --- Botón Ingresar ---
        self.boton_login = QPushButton("Ingresar")
        self.boton_login.setCursor(Qt.CursorShape.PointingHandCursor)
        self.boton_login.setStyleSheet("""
            QPushButton { 
                background-color: #C5650D; 
                color: white; 
                border: none; 
                border-radius: 22px; /* Cambiado de 6px a 22px para efecto píldora */
                padding: 13px; 
                font-weight: bold; 
                font-size: 15px; 
                margin-top: 30px; 
            }
            QPushButton:hover { 
                background-color: #C06513; 
            }
            QPushButton:pressed { 
                background-color: #CC5500; 
            }
        """)
        self.boton_login.clicked.connect(self.procesar_login)
        layout_card.addWidget(self.boton_login)

        layout_principal.addWidget(self.card)
        self.setLayout(layout_principal)

        sombra = QGraphicsDropShadowEffect(self)
        sombra.setBlurRadius(30)
        sombra.setXOffset(0)
        sombra.setYOffset(8)
        sombra.setColor("#60000000")  # Sombra un poco más densa
        self.card.setGraphicsEffect(sombra)

        self.centrar_ventana()

    def alternar_contrasena(self):
        """Alterna la visibilidad de la contraseña y cambia el ícono del QAction."""
        ruta_ver = os.path.join(os.path.dirname(__file__), 'ver.png')
        ruta_ocultar = os.path.join(os.path.dirname(__file__), 'ocultar.png')

        if self.input_contrasena.echoMode() == QLineEdit.EchoMode.Password:
            self.input_contrasena.setEchoMode(QLineEdit.EchoMode.Normal)
            self.accion_ver_pass.setIcon(QIcon(ruta_ocultar))
        else:
            self.input_contrasena.setEchoMode(QLineEdit.EchoMode.Password)
            self.accion_ver_pass.setIcon(QIcon(ruta_ver))

    def procesar_login(self):
        usuario = self.input_usuario.text()
        contrasena = self.input_contrasena.text()

        db = GestorBD()
        rol = db.validar_usuario(usuario, contrasena)

        if rol == 'admin':
            self.nueva_ventana = VentanaAdmin()
            self.nueva_ventana.show()
            self.close()
        elif rol == 'vendedor':
            self.nueva_ventana = VentanaVendedor()
            self.nueva_ventana.show()
            self.close()
        else:
            QMessageBox.warning(self, "Error de Acceso", "Usuario o contraseña incorrectos.")
            self.input_contrasena.clear()