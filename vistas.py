import os, re

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                               QPushButton, QFrame, QMessageBox, QGraphicsDropShadowEffect,
                               QTableWidget, QTableWidgetItem, QHeaderView, QTabWidget,
                               QDateEdit, QTimeEdit, QScrollArea, QStackedWidget,
                               QGridLayout, QComboBox, QRadioButton, QButtonGroup, QGroupBox,QSizePolicy,QStackedWidget,QProgressBar, QCheckBox,QInputDialog)

from PySide6.QtGui import QPixmap, QIcon, QAction, QColor,QIntValidator
from database import GestorBD
from PySide6.QtWidgets import QDialog,QDateEdit, QTimeEdit
from PySide6.QtCore import Qt, QSize, Signal,QDate, QTime


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


class VentanaAdmin(VentanaBase):
    def __init__(self, usuario_info):
        # Aumentamos el tamaño para que quepa bien la tabla
        super().__init__("Panel Administrativo - Excellence Cocinas", 1000, 700)

        layout_principal = QVBoxLayout(self)

        # Saludo y encabezado
        header = QHBoxLayout()
        saludo = QLabel(f"Bienvenido, <b>{usuario_info['nombre']}</b> (Admin)")
        saludo.setStyleSheet("font-size: 14px;")

        self.boton_logout = QPushButton("Cerrar Sesión")
        self.boton_logout.setFixedSize(120, 30)
        self.boton_logout.setStyleSheet("background-color: #E74C3C; color: white; border-radius: 5px;")
        self.boton_logout.clicked.connect(self.cerrar_sesion)

        header.addWidget(saludo)
        header.addStretch()
        header.addWidget(self.boton_logout)
        layout_principal.addLayout(header)

        # --- SISTEMA DE PESTAÑAS ---
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabBar::tab { height: 40px; width: 200px; font-weight: bold; }
            QTabBar::tab:selected { color: #EF7C0F; border-bottom: 2px solid #EF7C0F; }
        """)

        # Pestaña 1: Prospectos
        self.tab_prospectos = PanelProspectos(usuario_info)
        self.tabs.addTab(self.tab_prospectos, "Prospectos y Clientes")

        # Pestaña 2: Inventario (Aquí pondrás tu tabla de materiales después)
        self.tab_inventario = QWidget()
        layout_inv = QVBoxLayout(self.tab_inventario)
        layout_inv.addWidget(QLabel("Aquí se gestionará el Inventario y Materiales"))
        self.tabs.addTab(self.tab_inventario, "Inventario / Materiales")

        layout_principal.addWidget(self.tabs)
        self.centrar_ventana()

class VentanaVendedor(VentanaBase):
    def __init__(self, usuario_info):
        # 1. Recibimos usuario_info y ajustamos el tamaño
        super().__init__("Módulo de Ventas - Excellence Cocinas", 1000, 700)

        layout_principal = QVBoxLayout(self)

        # --- Saludo y encabezado ---
        header = QHBoxLayout()
        saludo = QLabel(f"Bienvenido, <b>{usuario_info['nombre']}</b> (Ventas)")
        saludo.setStyleSheet("font-size: 14px; color: #333;")

        self.boton_logout = QPushButton("Cerrar Sesión")
        self.boton_logout.setFixedSize(120, 30)
        self.boton_logout.setStyleSheet(
            "background-color: #E74C3C; color: white; border-radius: 5px; font-weight: bold;")
        self.boton_logout.clicked.connect(self.cerrar_sesion)

        header.addWidget(saludo)
        header.addStretch()
        header.addWidget(self.boton_logout)
        layout_principal.addLayout(header)

        # --- SISTEMA DE PESTAÑAS ---
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabBar::tab { height: 40px; width: 200px; font-weight: bold; }
            QTabBar::tab:selected { color: #EF7C0F; border-bottom: 2px solid #EF7C0F; }
        """)

        # Pestaña 1: Mis Prospectos (Filtra automáticamente)
        self.tab_prospectos = PanelProspectos(usuario_info)
        self.tabs.addTab(self.tab_prospectos, "Mis Prospectos")

        # Pestaña 2: Cotizaciones
        self.tab_cotizaciones = QWidget()
        layout_cot = QVBoxLayout(self.tab_cotizaciones)
        layout_cot.addWidget(QLabel("Aquí generaremos las nuevas cotizaciones y PDFs"))
        self.tabs.addTab(self.tab_cotizaciones, "Cotizaciones")

        layout_principal.addWidget(self.tabs)
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

        if not usuario or not contrasena:
            QMessageBox.warning(self, "Campos vacíos", "Por favor ingresa todos los datos.")
            return

        db = GestorBD()
        resultado = db.validar_usuario(usuario, contrasena)

        if resultado:
            # Empaquetamos la info en un diccionario para pasarlo fácil entre ventanas
            usuario_info = {
                'id': resultado[0],
                'nombre': resultado[1],
                'rol': resultado[2]
            }

            if usuario_info['rol'] == 'admin':
                self.nueva_ventana = VentanaAdmin(usuario_info)
            elif usuario_info['rol'] == 'vendedor':
                self.nueva_ventana = VentanaVendedor(usuario_info)

            self.nueva_ventana.show()
            self.close()
        else:
            QMessageBox.warning(self, "Error de Acceso", "Usuario o contraseña incorrectos.")
            self.input_contrasena.clear()




# -------------------------------------------------------
# WIDGET: Tarjeta individual de un prospecto/cliente
# -------------------------------------------------------
class TarjetaProspecto(QFrame):
    """Card clickeable que muestra nombre, teléfono y barra de progreso."""

    clicked = Signal(int)  # Emite el prospecto_id al hacer click

    PASOS = ["Contacto inicial", "Medición", "Diseño enviado", "Cotización aceptada", "Cliente"]

    def __init__(self, prospecto_id, nombre, telefono, pasos_completados):
        super().__init__()
        self.prospecto_id = prospecto_id
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(100)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self._aplicar_estilo(False)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(6)

        # Fila superior: nombre y teléfono
        fila_top = QHBoxLayout()
        lbl_nombre = QLabel(f"<b>{nombre}</b>")
        lbl_nombre.setStyleSheet("font-size: 14px; color: #2C3E50; background: transparent;")
        lbl_tel = QLabel(f"📞 {telefono or 'Sin teléfono'}")
        lbl_tel.setStyleSheet("font-size: 12px; color: #7F8C8D; background: transparent;")
        fila_top.addWidget(lbl_nombre)
        fila_top.addStretch()
        fila_top.addWidget(lbl_tel)
        layout.addLayout(fila_top)

        # Barra de progreso
        total = len(self.PASOS)
        completados = pasos_completados
        porcentaje = int((completados / total) * 100)

        barra = QProgressBar()
        barra.setRange(0, 100)
        barra.setValue(porcentaje)
        barra.setTextVisible(False)
        barra.setFixedHeight(8)
        color_barra = "#27AE60" if porcentaje == 100 else "#EF7C0F"
        barra.setStyleSheet(f"""
            QProgressBar {{ background-color: #ECF0F1; border-radius: 4px; border: none; }}
            QProgressBar::chunk {{ background-color: {color_barra}; border-radius: 4px; }}
        """)
        layout.addWidget(barra)

        # Texto de progreso
        paso_actual = self.PASOS[min(completados, total - 1)]
        lbl_paso = QLabel(f"Paso {completados}/{total} — {paso_actual}")
        lbl_paso.setStyleSheet("font-size: 11px; color: #95A5A6; background: transparent;")
        layout.addWidget(lbl_paso)

    def _aplicar_estilo(self, hover):
        color = "#F0F4F8" if hover else "#FFFFFF"
        self.setStyleSheet(f"""
            TarjetaProspecto {{
                background-color: {color};
                border: 1px solid #E0E6ED;
                border-radius: 10px;
            }}
        """)

    def enterEvent(self, event):
        self._aplicar_estilo(True)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._aplicar_estilo(False)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.prospecto_id)
        super().mousePressEvent(event)



class DetalleProspecto(QWidget):
    """Panel lateral que muestra los 5 pasos con checkboxes y barra de progreso."""

    cerrado = Signal()  # Para volver a la lista

    PASOS = ["Contacto inicial", "Medición", "Diseño enviado", "Cotización aceptada", "Cliente"]

    def __init__(self, prospecto_id, nombre, telefono):
        super().__init__()
        self.prospecto_id = prospecto_id
        self.db = GestorBD()

        # Asegurar que el checklist existe
        self.db.inicializar_checklist_prospecto(prospecto_id)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        # Botón volver
        btn_volver = QPushButton("← Volver")
        btn_volver.setFixedSize(100, 30)
        btn_volver.setStyleSheet("""
            QPushButton { background: transparent; color: #EF7C0F; border: none; 
                          font-weight: bold; font-size: 13px; text-align: left; }
            QPushButton:hover { color: #C06513; }
        """)
        btn_volver.clicked.connect(self.cerrado.emit)
        layout.addWidget(btn_volver)

        # Nombre y teléfono
        lbl_nombre = QLabel(f"<b style='font-size:18px;'>{nombre}</b>")
        lbl_nombre.setStyleSheet("color: #2C3E50;")
        lbl_tel = QLabel(f"📞 {telefono or 'Sin teléfono'}")
        lbl_tel.setStyleSheet("color: #7F8C8D; font-size: 13px;")
        layout.addWidget(lbl_nombre)
        layout.addWidget(lbl_tel)

        # Separador
        linea = QFrame()
        linea.setFrameShape(QFrame.Shape.HLine)
        linea.setStyleSheet("color: #E0E6ED;")
        layout.addWidget(linea)

        # Título sección
        lbl_seguimiento = QLabel("Seguimiento del proceso")
        lbl_seguimiento.setStyleSheet("font-size: 14px; font-weight: bold; color: #2C3E50;")
        layout.addWidget(lbl_seguimiento)

        # Barra de progreso grande
        self.barra_grande = QProgressBar()
        self.barra_grande.setRange(0, 100)
        self.barra_grande.setFixedHeight(14)
        self.barra_grande.setStyleSheet("""
            QProgressBar { background-color: #ECF0F1; border-radius: 7px; border: none; }
            QProgressBar::chunk { background-color: #EF7C0F; border-radius: 7px; }
        """)
        layout.addWidget(self.barra_grande)

        # Label porcentaje
        self.lbl_porcentaje = QLabel()
        self.lbl_porcentaje.setStyleSheet("color: #7F8C8D; font-size: 12px;")
        self.lbl_porcentaje.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.lbl_porcentaje)

        # Checkboxes de pasos
        self.checkboxes = []
        checklist = self.db.obtener_checklist(prospecto_id)

        frame_pasos = QFrame()
        frame_pasos.setStyleSheet("background-color: #F8FAFB; border-radius: 10px;")
        layout_pasos = QVBoxLayout(frame_pasos)
        layout_pasos.setContentsMargins(16, 12, 16, 12)
        layout_pasos.setSpacing(10)

        for item_id, paso_nombre, completado in checklist:
            cb = QCheckBox(paso_nombre)
            cb.setChecked(bool(completado))
            cb.setProperty("checklist_id", item_id)
            cb.setStyleSheet("""
                QCheckBox { font-size: 14px; color: #2C3E50; spacing: 10px; }
                QCheckBox::indicator { width: 20px; height: 20px; border-radius: 10px; 
                                       border: 2px solid #BDC3C7; background: white; }
                QCheckBox::indicator:checked { background-color: #27AE60; border-color: #27AE60; }
                QCheckBox:checked { color: #27AE60; text-decoration: line-through; }
            """)
            cb.stateChanged.connect(self._actualizar_paso)
            self.checkboxes.append(cb)
            layout_pasos.addWidget(cb)

        layout.addWidget(frame_pasos)
        layout.addStretch()

        self._actualizar_progreso()

    def _actualizar_paso(self):
        """Guarda el cambio en BD y refresca la barra."""
        sender = self.sender()
        checklist_id = sender.property("checklist_id")
        completado = 1 if sender.isChecked() else 0
        self.db.actualizar_paso_checklist(checklist_id, completado)

        # Si el último paso se marca, convertir a cliente
        todos = all(cb.isChecked() for cb in self.checkboxes)
        if todos:
            self.db.marcar_como_cliente(self.prospecto_id)

        self._actualizar_progreso()

    def _actualizar_progreso(self):
        completados = sum(1 for cb in self.checkboxes if cb.isChecked())
        total = len(self.checkboxes)
        porcentaje = int((completados / total) * 100)
        self.barra_grande.setValue(porcentaje)
        self.lbl_porcentaje.setText(f"{completados} de {total} pasos completados — {porcentaje}%")

        # Color verde cuando está completo
        if porcentaje == 100:
            self.barra_grande.setStyleSheet("""
                QProgressBar { background-color: #ECF0F1; border-radius: 7px; border: none; }
                QProgressBar::chunk { background-color: #27AE60; border-radius: 7px; }
            """)


# -------------------------------------------------------
# WIDGET: Tarjeta individual de un prospecto/cliente

# -------------------------------------------------------
class TarjetaProspecto(QFrame):
    clicked = Signal(int)

    def __init__(self, prospecto_id, nombre, telefono, cita_info):
        super().__init__()
        self.prospecto_id = prospecto_id
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(105)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self._aplicar_estilo(False)

        self.sombra = QGraphicsDropShadowEffect(self)
        self.sombra.setBlurRadius(15)
        self.sombra.setYOffset(4)
        self.sombra.setColor(QColor(0, 0, 0, 20))
        self.setGraphicsEffect(self.sombra)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)

        fila_top = QHBoxLayout()
        lbl_nombre = QLabel(f"<b>{nombre}</b>")
        lbl_nombre.setStyleSheet("font-size: 15px; color: #1E293B; background: transparent;")
        lbl_tel = QLabel(f"📞 {telefono}")
        lbl_tel.setStyleSheet("font-size: 13px; font-weight: bold; color: #64748B; background: transparent;")

        fila_top.addWidget(lbl_nombre)
        fila_top.addStretch()
        fila_top.addWidget(lbl_tel)
        layout.addLayout(fila_top)

        # Estado visual basado en la Cita
        if cita_info:
            fecha, hora = cita_info
            lbl_estado = QLabel(f"📅 Cita programada: {fecha} a las {hora}")
            lbl_estado.setStyleSheet("font-size: 13px; font-weight: bold; color: #EF7C0F; background: transparent;")
        else:
            lbl_estado = QLabel("⏳ Nuevo - Pendiente de agendar cita")
            lbl_estado.setStyleSheet("font-size: 13px; font-weight: 500; color: #94A3B8; background: transparent;")

        layout.addWidget(lbl_estado)

    def _aplicar_estilo(self, hover):
        fondo = "#F8FAFC" if hover else "#FFFFFF"
        borde = "1px solid #CBD5E1" if hover else "1px solid transparent"
        self.setStyleSheet(f"TarjetaProspecto {{ background-color: {fondo}; border: {borde}; border-radius: 12px; }}")

    def enterEvent(self, event):
        self._aplicar_estilo(True)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._aplicar_estilo(False)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.prospecto_id)
        super().mousePressEvent(event)

# -------------------------------------------------------
# WIDGET: Detalle de un prospecto con checklist visual
# -------------------------------------------------------
class DetalleProspecto(QWidget):
    cerrado = Signal()

    def __init__(self, prospecto_id, nombre, telefono):
        super().__init__()
        self.prospecto_id = prospecto_id
        self.db = GestorBD()

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("DetalleProspecto { background-color: #F8F9FB; }")

        # Usamos un ScrollArea principal por si la pantalla del vendedor es pequeña
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        contenedor_scroll = QWidget()
        contenedor_scroll.setStyleSheet("background: transparent;")
        self.layout = QVBoxLayout(contenedor_scroll)
        self.layout.setContentsMargins(30, 25, 30, 25)
        self.layout.setSpacing(15)

        # --- BOTÓN VOLVER Y HEADER ---
        btn_volver = QPushButton("← Volver a la lista")
        btn_volver.setFixedSize(140, 35)
        btn_volver.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_volver.setStyleSheet("""
            QPushButton { background-color: white; color: #EF7C0F; border: 1px solid #EF7C0F; border-radius: 6px; font-weight: bold; font-size: 13px; }
            QPushButton:hover { background-color: #EF7C0F; color: white; }
        """)
        btn_volver.clicked.connect(self.cerrado.emit)
        self.layout.addWidget(btn_volver)

        card_header = QFrame()
        card_header.setStyleSheet("background-color: white; border-radius: 10px; border: 1px solid #E2E8F0;")
        layout_header = QVBoxLayout(card_header)
        lbl_nombre = QLabel(f"{nombre}")
        lbl_nombre.setStyleSheet("font-size: 22px; font-weight: bold; color: #1E293B; border: none;")
        lbl_tel = QLabel(f"📞 {telefono}")
        lbl_tel.setStyleSheet("font-size: 14px; font-weight: bold; color: #64748B; border: none;")
        layout_header.addWidget(lbl_nombre)
        layout_header.addWidget(lbl_tel)
        self.layout.addWidget(card_header)

        # ==========================================
        # FASE 1: AGENDAR CITA (Se mantiene intacta)
        # ==========================================
        self._construir_fase1()

        # ==========================================
        # FASE 2: LEVANTAMIENTO Y MEDICIÓN
        # ==========================================
        self._construir_fase2()

        self.layout.addStretch()
        scroll.setWidget(contenedor_scroll)
        layout_principal.addWidget(scroll)

    def _construir_fase1(self):
        lbl_fase1 = QLabel("Fase 1: Agendar Cita")
        lbl_fase1.setStyleSheet("font-size: 16px; font-weight: bold; color: #1E293B; margin-top: 10px;")
        self.layout.addWidget(lbl_fase1)

        frame_cita = QFrame()
        frame_cita.setFixedHeight(105)
        frame_cita.setStyleSheet("QFrame { background-color: white; border-radius: 12px; border: 1px solid #E2E8F0; }")

        layout_cita = QHBoxLayout(frame_cita)
        layout_cita.setContentsMargins(25, 15, 25, 15)
        layout_cita.setSpacing(25)

        estilo_inputs = """
            QDateEdit, QTimeEdit { background-color: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 5px; padding: 4px 10px; color: #1E293B; font-size: 14px; }
            QDateEdit:focus, QTimeEdit:focus { border: 1px solid #EF7C0F; }
            QDateEdit::drop-down { subcontrol-origin: padding; subcontrol-position: top right; width: 25px; border-left: 1px solid #CBD5E1; background-color: #F8FAFC; border-top-right-radius: 4px; border-bottom-right-radius: 4px; }
            QDateEdit::down-arrow { image: none; border-left: 5px solid transparent; border-right: 5px solid transparent; border-top: 6px solid #475569; width: 0px; height: 0px; }
            QTimeEdit::up-button, QTimeEdit::down-button { subcontrol-origin: border; width: 25px; background-color: #F8FAFC; border-left: 1px solid #CBD5E1; }
            QTimeEdit::up-button { subcontrol-position: top right; border-top-right-radius: 4px; border-bottom: 1px solid #CBD5E1; }
            QTimeEdit::down-button { subcontrol-position: bottom right; border-bottom-right-radius: 4px; }
            QTimeEdit::up-arrow { image: none; border-left: 4px solid transparent; border-right: 4px solid transparent; border-bottom: 5px solid #475569; width: 0px; height: 0px; }
            QTimeEdit::down-arrow { image: none; border-left: 4px solid transparent; border-right: 4px solid transparent; border-top: 5px solid #475569; width: 0px; height: 0px; }
        """

        columna_fecha = QVBoxLayout()
        columna_fecha.setSpacing(5)
        lbl_fecha = QLabel("📅 Fecha:")
        lbl_fecha.setStyleSheet("font-size: 13px; font-weight: bold; color: #64748B; border: none;")
        self.input_fecha = QDateEdit(QDate.currentDate())
        self.input_fecha.setCalendarPopup(True)
        self.input_fecha.setDisplayFormat("dd/MM/yyyy")
        self.input_fecha.setFixedSize(140, 36)
        self.input_fecha.setStyleSheet(estilo_inputs)
        columna_fecha.addWidget(lbl_fecha)
        columna_fecha.addWidget(self.input_fecha)

        columna_hora = QVBoxLayout()
        columna_hora.setSpacing(5)
        lbl_hora = QLabel("⏰ Hora:")
        lbl_hora.setStyleSheet("font-size: 13px; font-weight: bold; color: #64748B; border: none;")
        self.input_hora = QTimeEdit(QTime.currentTime())
        self.input_hora.setDisplayFormat("hh:mm AP")
        self.input_hora.setFixedSize(120, 36)
        self.input_hora.setStyleSheet(estilo_inputs)
        columna_hora.addWidget(lbl_hora)
        columna_hora.addWidget(self.input_hora)

        columna_boton = QVBoxLayout()
        columna_boton.setAlignment(Qt.AlignmentFlag.AlignBottom)
        btn_agendar = QPushButton("Guardar Cita")
        btn_agendar.setFixedSize(140, 36)
        btn_agendar.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_agendar.setStyleSheet(
            "QPushButton { background-color: #27AE60; color: white; font-weight: bold; font-size: 13px; border-radius: 6px; border: none; } QPushButton:hover { background-color: #219653; }")
        btn_agendar.clicked.connect(self._guardar_cita)
        columna_boton.addWidget(btn_agendar)

        layout_cita.addLayout(columna_fecha)
        layout_cita.addLayout(columna_hora)
        layout_cita.addStretch()
        layout_cita.addLayout(columna_boton)
        self.layout.addWidget(frame_cita)

        cita_existente = self.db.obtener_cita(self.prospecto_id)
        if cita_existente:
            fecha_str, hora_str = cita_existente
            self.input_fecha.setDate(QDate.fromString(fecha_str, "dd/MM/yyyy"))
            self.input_hora.setTime(QTime.fromString(hora_str, "hh:mm AP"))
            lbl_fase1.setText("Fase 1: Cita Agendada ✅")
            lbl_fase1.setStyleSheet("font-size: 16px; font-weight: bold; color: #27AE60; margin-top: 10px;")
            btn_agendar.setText("Actualizar Cita")
            btn_agendar.setStyleSheet(
                "QPushButton { background-color: #EF7C0F; color: white; font-weight: bold; font-size: 13px; border-radius: 6px; border: none; } QPushButton:hover { background-color: #C06513; }")

    def _guardar_cita(self):
        fecha = self.input_fecha.date().toString("dd/MM/yyyy")
        hora = self.input_hora.time().toString("hh:mm AP")
        self.db.agendar_cita(self.prospecto_id, fecha, hora)
        QMessageBox.information(self, "Éxito", "La cita se ha agendado correctamente.")
        self.cerrado.emit()

    def _construir_fase2(self):
        lbl_fase2 = QLabel("Fase 2: Levantamiento y Medición")
        lbl_fase2.setStyleSheet("font-size: 16px; font-weight: bold; color: #1E293B; margin-top: 20px;")
        self.layout.addWidget(lbl_fase2)

        self.tabs_medicion = QTabWidget()
        self.tabs_medicion.setStyleSheet("""
            QTabWidget::pane { border: 1px solid #E2E8F0; background: white; border-radius: 8px; }
            QTabBar::tab { background: #F1F5F9; color: #64748B; padding: 10px 15px; font-weight: bold; border-top-left-radius: 6px; border-top-right-radius: 6px; margin-right: 2px; }
            QTabBar::tab:selected { background: white; color: #EF7C0F; border-bottom: 2px solid white; }
        """)

        # --- ESTILOS ESTRICTOS CORREGIDOS ---
        estilo_label = "font-size: 13px; font-weight: bold; color: #475569;"
        estilo_input = """
            QLineEdit, QComboBox, QDateEdit { 
                background-color: #F8FAFC; border: 1px solid #CBD5E1; border-radius: 5px; 
                padding: 6px; color: #1E293B; font-size: 13px;
            }
            QLineEdit:focus, QComboBox:focus, QDateEdit:focus { border: 1px solid #EF7C0F; }
            QDateEdit::drop-down { border: none; width: 20px; }

            /* Corrección para que el menú desplegable no se vea negro en modo oscuro */
            QComboBox QAbstractItemView { 
                background-color: #FFFFFF; 
                color: #1E293B; 
                selection-background-color: #27AE60; 
                selection-color: white; 
                outline: none;
            }
        """

        def crear_label(texto):
            lbl = QLabel(texto)
            lbl.setStyleSheet(estilo_label)
            return lbl

        # --- Pestaña 1: Datos Generales ---
        tab_generales = QWidget()
        layout_gen = QGridLayout(tab_generales)
        layout_gen.setContentsMargins(20, 20, 20, 20)
        layout_gen.setSpacing(15)

        self.in_fecha_visita = QDateEdit(QDate.currentDate());
        self.in_fecha_visita.setCalendarPopup(True);
        self.in_fecha_visita.setDisplayFormat("dd/MM/yyyy");
        self.in_fecha_visita.setStyleSheet(estilo_input)
        self.cb_pago_visita = QComboBox();
        self.cb_pago_visita.addItems(["NO", "SÍ"]);
        self.cb_pago_visita.setStyleSheet(estilo_input)

        # Validadores Numéricos
        from PySide6.QtGui import QIntValidator  # Aseguramos la importación aquí por si acaso
        validador_dinero = QIntValidator(0, 999999)

        self.in_importe_visita = QLineEdit();
        self.in_importe_visita.setPlaceholderText("$");
        self.in_importe_visita.setValidator(validador_dinero);
        self.in_importe_visita.setStyleSheet(estilo_input)
        self.in_importe_3d = QLineEdit();
        self.in_importe_3d.setPlaceholderText("$");
        self.in_importe_3d.setValidator(validador_dinero);
        self.in_importe_3d.setStyleSheet(estilo_input)

        self.in_fraccionamiento = QLineEdit();
        self.in_fraccionamiento.setStyleSheet(estilo_input)
        self.in_prototipo = QLineEdit();
        self.in_prototipo.setPlaceholderText("Ej. Modelo Albatros");
        self.in_prototipo.setStyleSheet(estilo_input)
        self.in_direccion = QLineEdit();
        self.in_direccion.setStyleSheet(estilo_input)

        self.cb_vive_ahi = QComboBox();
        self.cb_vive_ahi.addItems(["SÍ", "NO"]);
        self.cb_vive_ahi.setStyleSheet(estilo_input)
        self.cb_entero = QComboBox();
        self.cb_entero.addItems(["Redes Sociales", "Recomendación", "Pasó por el local", "Otro"]);
        self.cb_entero.setStyleSheet(estilo_input)
        self.cb_entero.currentTextChanged.connect(self._manejar_opcion_otro)

        layout_gen.addWidget(crear_label("Fecha Visita:"), 0, 0)
        layout_gen.addWidget(self.in_fecha_visita, 0, 1)
        layout_gen.addWidget(crear_label("¿Pagó Visita Técnica?:"), 0, 2)
        layout_gen.addWidget(self.cb_pago_visita, 0, 3)

        layout_gen.addWidget(crear_label("Importe Visita:"), 1, 0)
        layout_gen.addWidget(self.in_importe_visita, 1, 1)
        layout_gen.addWidget(crear_label("Importe 3D:"), 1, 2)
        layout_gen.addWidget(self.in_importe_3d, 1, 3)

        layout_gen.addWidget(crear_label("Fraccionamiento:"), 2, 0)
        layout_gen.addWidget(self.in_fraccionamiento, 2, 1)
        layout_gen.addWidget(crear_label("Modelo/Prototipo:"), 2, 2)
        layout_gen.addWidget(self.in_prototipo, 2, 3)

        layout_gen.addWidget(crear_label("Dirección Exacta:"), 3, 0)
        layout_gen.addWidget(self.in_direccion, 3, 1, 1, 3)

        layout_gen.addWidget(crear_label("¿Vive ahí?:"), 4, 0)
        layout_gen.addWidget(self.cb_vive_ahi, 4, 1)
        layout_gen.addWidget(crear_label("¿Cómo se enteró?:"), 4, 2)
        layout_gen.addWidget(self.cb_entero, 4, 3)

        self.tabs_medicion.addTab(tab_generales, "📝 Generales")

        # --- Pestaña 2: Diseño y Presupuesto ---
        tab_diseno = QWidget()
        layout_diseno = QGridLayout(tab_diseno)
        layout_diseno.setContentsMargins(20, 20, 20, 20)
        layout_diseno.setSpacing(15)

        self.cb_presupuesto = QComboBox();
        self.cb_presupuesto.addItems(
            ["$60k - $80k", "$80k - $120k", "$120k - $200k", "$200k - $250k", "$250k - $300k", "Más de $300k"]);
        self.cb_presupuesto.setStyleSheet(estilo_input)
        self.cb_equipos_inc = QComboBox();
        self.cb_equipos_inc.addItems(["SÍ", "NO"]);
        self.cb_equipos_inc.setStyleSheet(estilo_input)
        self.cb_facilidades = QComboBox();
        self.cb_facilidades.addItems(["NA", "Etapas", "Parcialidades", "MSI"]);
        self.cb_facilidades.setStyleSheet(estilo_input)

        self.cb_ya_tiene = QComboBox();
        self.cb_ya_tiene.addItems(["NO", "SÍ"]);
        self.cb_ya_tiene.setStyleSheet(estilo_input)
        self.cb_distribucion = QComboBox();
        self.cb_distribucion.addItems(["Barra", "Isla", "Lineal", "Forma L", "Forma U", "NA"]);
        self.cb_distribucion.setStyleSheet(estilo_input)
        self.cb_altura = QComboBox();
        self.cb_altura.addItems(["2.40", "2.20", "Otra"]);
        self.cb_altura.setStyleSheet(estilo_input)
        self.cb_plafon = QComboBox();
        self.cb_plafon.addItems(["NO", "SÍ"]);
        self.cb_plafon.setStyleSheet(estilo_input)

        layout_diseno.addWidget(crear_label("Rango de Presupuesto:"), 0, 0)
        layout_diseno.addWidget(self.cb_presupuesto, 0, 1)
        layout_diseno.addWidget(crear_label("¿Contempla equipos?:"), 0, 2)
        layout_diseno.addWidget(self.cb_equipos_inc, 0, 3)

        layout_diseno.addWidget(crear_label("Facilidades de pago:"), 1, 0)
        layout_diseno.addWidget(self.cb_facilidades, 1, 1)

        layout_diseno.addWidget(crear_label("¿Ya tiene cocina?:"), 2, 0)
        layout_diseno.addWidget(self.cb_ya_tiene, 2, 1)
        layout_diseno.addWidget(crear_label("Distribución deseada:"), 2, 2)
        layout_diseno.addWidget(self.cb_distribucion, 2, 3)

        layout_diseno.addWidget(crear_label("Altura deseada:"), 3, 0)
        layout_diseno.addWidget(self.cb_altura, 3, 1)
        layout_diseno.addWidget(crear_label("¿Desea plafón con luz?:"), 3, 2)
        layout_diseno.addWidget(self.cb_plafon, 3, 3)

        layout_diseno.setRowStretch(4, 1)
        self.tabs_medicion.addTab(tab_diseno, "📐 Diseño y Presupuesto")

        # --- Pestaña 3: Acabados ---
        tab_acabados = QWidget()
        layout_aca = QGridLayout(tab_acabados)
        layout_aca.setContentsMargins(20, 20, 20, 20)
        layout_aca.setSpacing(15)

        self.in_puertas1 = QLineEdit();
        self.in_puertas1.setStyleSheet(estilo_input)
        self.in_puertas2 = QLineEdit();
        self.in_puertas2.setStyleSheet(estilo_input)
        self.in_cubierta_a = QLineEdit();
        self.in_cubierta_a.setStyleSheet(estilo_input)
        self.in_cubierta_b = QLineEdit();
        self.in_cubierta_b.setStyleSheet(estilo_input)
        self.in_jaladeras = QLineEdit();
        self.in_jaladeras.setStyleSheet(estilo_input)
        self.cb_zoclo = QComboBox();
        self.cb_zoclo.addItems(["NEGRO", "INOX", "CONCRETO", "OTRO"]);
        self.cb_zoclo.setStyleSheet(estilo_input)
        self.in_extras = QLineEdit();
        self.in_extras.setStyleSheet(estilo_input)

        layout_aca.addWidget(crear_label("Opción 1 Puertas:"), 0, 0)
        layout_aca.addWidget(self.in_puertas1, 0, 1)
        layout_aca.addWidget(crear_label("Opción 2 Puertas:"), 1, 0)
        layout_aca.addWidget(self.in_puertas2, 1, 1)

        layout_aca.addWidget(crear_label("Cubierta A:"), 2, 0)
        layout_aca.addWidget(self.in_cubierta_a, 2, 1)
        layout_aca.addWidget(crear_label("Cubierta B:"), 3, 0)
        layout_aca.addWidget(self.in_cubierta_b, 3, 1)

        layout_aca.addWidget(crear_label("Jaladeras:"), 4, 0)
        layout_aca.addWidget(self.in_jaladeras, 4, 1)
        layout_aca.addWidget(crear_label("Zoclo / Base:"), 5, 0)
        layout_aca.addWidget(self.cb_zoclo, 5, 1)

        layout_aca.addWidget(crear_label("Extras:"), 6, 0)
        layout_aca.addWidget(self.in_extras, 6, 1)

        self.tabs_medicion.addTab(tab_acabados, "🎨 Acabados")

        # --- Pestaña 4: Equipamiento ---
        tab_equipos = QWidget()
        layout_equipos = QGridLayout(tab_equipos)
        layout_equipos.setContentsMargins(20, 20, 20, 20)
        layout_equipos.setSpacing(10)

        equipos_lista = [
            ("Tarja", "Ej: 1 o 2 tinas..."),
            ("Monomando", "Especificaciones..."),
            ("Horno", "Gas/Eléctrico, 60/80cm..."),
            ("Refrigerador", "Medidas, modelo..."),
            ("Estufa/Parrilla", "Inducción/Gas, 90cm..."),
            ("Campana", "Empotre, diseño..."),
            ("Microondas", "Especificaciones..."),
            ("Lavavajillas", "Especificaciones..."),
            ("Triturador", "Especificaciones..."),
            ("Filtro de agua", "Especificaciones...")
        ]
        self.inputs_equipos = {}

        layout_equipos.addWidget(crear_label("EQUIPO"), 0, 0)
        layout_equipos.addWidget(crear_label("ESTADO"), 0, 1)
        layout_equipos.addWidget(crear_label("ESPECIFICACIONES / DETALLES"), 0, 2)

        for i, (equipo, placeholder) in enumerate(equipos_lista, start=1):
            layout_equipos.addWidget(crear_label(equipo), i, 0)
            cb_estado = QComboBox();
            cb_estado.addItems(["No usa", "Proponer", "Ya tiene"]);
            cb_estado.setStyleSheet(estilo_input)
            in_detalle = QLineEdit();
            in_detalle.setPlaceholderText(placeholder);
            in_detalle.setStyleSheet(estilo_input)
            self.inputs_equipos[equipo] = (cb_estado, in_detalle)
            layout_equipos.addWidget(cb_estado, i, 1)
            layout_equipos.addWidget(in_detalle, i, 2)

        self.tabs_medicion.addTab(tab_equipos, "🔌 Equipos")
        self.layout.addWidget(self.tabs_medicion)

        # --- Botón para guardar ---
        btn_guardar_fase2 = QPushButton("Guardar Formulario de Medición")
        btn_guardar_fase2.setFixedHeight(40)
        btn_guardar_fase2.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_guardar_fase2.setStyleSheet(
            "QPushButton { background-color: #2C3E50; color: white; font-weight: bold; font-size: 14px; border-radius: 6px; margin-top: 10px; } QPushButton:hover { background-color: #1A252F; }")
        btn_guardar_fase2.clicked.connect(self._guardar_medicion)
        self.layout.addWidget(btn_guardar_fase2)

        self._cargar_datos_medicion()

    def _manejar_opcion_otro(self, texto):
        if texto == "Otro":
            from PySide6.QtWidgets import QInputDialog
            nuevo_valor, ok = QInputDialog.getText(self, "Especificar", "¿Cómo se enteró de nosotros?")
            if ok and nuevo_valor.strip():
                combo = self.sender()
                combo.insertItem(combo.count() - 1, nuevo_valor.strip())
                combo.setCurrentText(nuevo_valor.strip())
            else:
                self.sender().setCurrentIndex(0)  # Si cancela, lo regresamos a la primera opción

    def _guardar_medicion(self):
        datos_generales = (
            self.in_fecha_visita.date().toString("dd/MM/yyyy"),
            self.cb_pago_visita.currentText(),
            self.in_importe_visita.text(),
            self.in_importe_3d.text(),
            self.in_fraccionamiento.text(),
            self.in_prototipo.text(),
            self.cb_vive_ahi.currentText(),
            self.in_direccion.text(),
            self.cb_entero.currentText(),
            ""  # Mantenemos el espacio vacío en BD por la eliminación de "cuando compra"
        )

        presupuesto = {
            "nivel": self.cb_presupuesto.currentText(),
            "equipos_incluidos": self.cb_equipos_inc.currentText(),
            "facilidades": self.cb_facilidades.currentText()
        }

        distribucion = {
            "ya_tiene": self.cb_ya_tiene.currentText(),
            "tipo": self.cb_distribucion.currentText(),
            "altura": self.cb_altura.currentText(),
            "plafon": self.cb_plafon.currentText()
        }

        acabados = {
            "puertas_1": self.in_puertas1.text(),
            "puertas_2": self.in_puertas2.text(),
            "cubierta_a": self.in_cubierta_a.text(),
            "cubierta_b": self.in_cubierta_b.text(),
            "jaladeras": self.in_jaladeras.text(),
            "zoclo": self.cb_zoclo.currentText(),
            "extras": self.in_extras.text()
        }

        equipos = {}
        for nombre, (cb_estado, in_detalle) in self.inputs_equipos.items():
            equipos[nombre] = {
                "estado": cb_estado.currentText(),
                "detalle": in_detalle.text()
            }

        self.db.guardar_medicion(self.prospecto_id, datos_generales, presupuesto, distribucion, acabados, equipos)
        QMessageBox.information(self, "Guardado",
                                "Formulario de medición guardado correctamente.\n¡Listo para generar PDF!")

    def _cargar_datos_medicion(self):
        datos = self.db.obtener_medicion(self.prospecto_id)
        if datos:
            (fv, pv, iv, i3d, frac, proto, vive, direc, entero, compra,
             presupuesto, distribucion, acabados, equipos) = datos

            if fv: self.in_fecha_visita.setDate(QDate.fromString(fv, "dd/MM/yyyy"))
            if pv: self.cb_pago_visita.setCurrentText(pv)
            if iv: self.in_importe_visita.setText(iv)
            if i3d: self.in_importe_3d.setText(i3d)
            if frac: self.in_fraccionamiento.setText(frac)
            if proto: self.in_prototipo.setText(proto)
            if vive: self.cb_vive_ahi.setCurrentText(vive)
            if direc: self.in_direccion.setText(direc)

            if entero:
                # Si el valor guardado no está en la lista estándar, lo agregamos temporalmente
                if self.cb_entero.findText(entero) == -1:
                    self.cb_entero.insertItem(self.cb_entero.count() - 1, entero)
                self.cb_entero.setCurrentText(entero)

            if presupuesto:
                if "nivel" in presupuesto: self.cb_presupuesto.setCurrentText(presupuesto["nivel"])
                if "equipos_incluidos" in presupuesto: self.cb_equipos_inc.setCurrentText(
                    presupuesto["equipos_incluidos"])
                if "facilidades" in presupuesto: self.cb_facilidades.setCurrentText(presupuesto["facilidades"])

            if distribucion:
                if "ya_tiene" in distribucion: self.cb_ya_tiene.setCurrentText(distribucion["ya_tiene"])
                if "tipo" in distribucion: self.cb_distribucion.setCurrentText(distribucion["tipo"])
                if "altura" in distribucion: self.cb_altura.setCurrentText(distribucion["altura"])
                if "plafon" in distribucion: self.cb_plafon.setCurrentText(distribucion["plafon"])

            if acabados:
                if "puertas_1" in acabados: self.in_puertas1.setText(acabados["puertas_1"])
                if "puertas_2" in acabados: self.in_puertas2.setText(acabados["puertas_2"])
                if "cubierta_a" in acabados: self.in_cubierta_a.setText(acabados["cubierta_a"])
                if "cubierta_b" in acabados: self.in_cubierta_b.setText(acabados["cubierta_b"])
                if "jaladeras" in acabados: self.in_jaladeras.setText(acabados["jaladeras"])
                if "zoclo" in acabados: self.cb_zoclo.setCurrentText(acabados["zoclo"])
                if "extras" in acabados: self.in_extras.setText(acabados["extras"])

            if equipos:
                for equipo, info in equipos.items():
                    if equipo in self.inputs_equipos:
                        cb_estado, in_detalle = self.inputs_equipos[equipo]
                        cb_estado.setCurrentText(info.get("estado", "No usa"))
                        in_detalle.setText(info.get("detalle", ""))
class DialogoNuevoProspecto(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nuevo Prospecto")
        self.setFixedSize(380, 260)
        self.setStyleSheet("background-color: white;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        lbl_titulo = QLabel("Registrar Nuevo Prospecto")
        lbl_titulo.setStyleSheet("font-size: 18px; font-weight: bold; color: #1E293B;")
        layout.addWidget(lbl_titulo)

        estilo_input = """
            QLineEdit { background-color: #F8FAFC; border: 1px solid #CBD5E1; border-radius: 6px; padding: 10px; font-size: 14px; color: #333; }
            QLineEdit:focus { border: 1px solid #EF7C0F; }
        """

        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Nombre completo del cliente")
        self.input_nombre.setStyleSheet(estilo_input)
        layout.addWidget(self.input_nombre)

        self.input_telefono = QLineEdit()
        self.input_telefono.setPlaceholderText("Teléfono (10 dígitos)")
        self.input_telefono.setStyleSheet(estilo_input)
        layout.addWidget(self.input_telefono)

        layout_botones = QHBoxLayout()
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_cancelar.setStyleSheet(
            "QPushButton { background-color: #F1F5F9; color: #475569; font-weight: bold; padding: 10px; border-radius: 6px; border: none; } QPushButton:hover { background-color: #E2E8F0; }")
        btn_cancelar.clicked.connect(self.reject)

        btn_guardar = QPushButton("Guardar Prospecto")
        btn_guardar.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_guardar.setStyleSheet(
            "QPushButton { background-color: #27AE60; color: white; font-weight: bold; padding: 10px; border-radius: 6px; border: none; } QPushButton:hover { background-color: #219653; }")

        # Conectamos a nuestro propio método de validación en lugar de accept directo
        btn_guardar.clicked.connect(self.validar_y_guardar)

        layout_botones.addWidget(btn_cancelar)
        layout_botones.addWidget(btn_guardar)

        layout.addStretch()
        layout.addLayout(layout_botones)

    def validar_y_guardar(self):
        nombre = self.input_nombre.text().strip()
        telefono = self.input_telefono.text().strip()

        # Validación de Nombre
        if len(nombre) < 3 or not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", nombre):
            QMessageBox.warning(self, "Error de Validación",
                                "El nombre debe tener al menos 3 letras y no contener números o caracteres especiales.")
            self.input_nombre.setFocus()
            return

        # Validación de Teléfono (Solo números, exacto 10 dígitos)
        tel_limpio = re.sub(r'\D', '', telefono)
        if len(tel_limpio) != 10:
            QMessageBox.warning(self, "Error de Validación",
                                "El número de teléfono debe contener exactamente 10 dígitos válidos.")
            self.input_telefono.setFocus()
            return

        # Si todo está bien, cerramos el diálogo con éxito
        self.accept()

    def obtener_datos(self):
        return self.input_nombre.text().strip(), re.sub(r'\D', '', self.input_telefono.text())

class PanelProspectos(QWidget):
    def __init__(self, usuario_info):
        super().__init__()
        self.usuario_id = usuario_info['id']
        self.es_admin = usuario_info['rol'] == 'admin'
        self.db = GestorBD()

        # Fondo general gris clarito para el panel completo
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("PanelProspectos { background-color: #F8F9FB; }")

        self.stack = QStackedWidget()
        layout_root = QVBoxLayout(self)
        layout_root.setContentsMargins(0, 0, 0, 0)
        layout_root.addWidget(self.stack)

        # --- Página 0: Lista ---
        pagina_lista = QWidget()
        layout_lista = QVBoxLayout(pagina_lista)
        layout_lista.setContentsMargins(20, 20, 20, 20)
        layout_lista.setSpacing(15)

        # Header
        header_layout = QHBoxLayout()
        titulo = QLabel("Seguimiento de Ventas")
        titulo.setStyleSheet("font-size: 22px; font-weight: bold; color: #1E293B;")

        self.btn_nuevo = QPushButton("+ Nuevo Prospecto")
        self.btn_nuevo.setFixedSize(160, 36)
        self.btn_nuevo.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_nuevo.setStyleSheet("""
            QPushButton { background-color: #27AE60; color: white; font-weight: bold; font-size: 13px; border-radius: 6px; border: none; }
            QPushButton:hover { background-color: #219653; }
        """)
        self.btn_nuevo.clicked.connect(self._abrir_formulario_nuevo)

        header_layout.addWidget(titulo)
        header_layout.addStretch()
        header_layout.addWidget(self.btn_nuevo)
        layout_lista.addLayout(header_layout)

        # Pestañas
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane { border: none; border-top: 1px solid #CBD5E1; }
            QTabBar::tab { height: 40px; width: 180px; font-weight: bold; color: #64748B; background: transparent; font-size: 14px; }
            QTabBar::tab:selected { color: #EF7C0F; border-bottom: 3px solid #EF7C0F; }
            QTabBar::tab:hover:!selected { color: #1E293B; }
        """)

        self.scroll_prospectos = self._crear_scroll()
        self.tabs.addTab(self.scroll_prospectos, "⏳ Prospectos en curso")

        self.scroll_clientes = self._crear_scroll()
        self.tabs.addTab(self.scroll_clientes, "✅ Clientes cerrados")

        layout_lista.addWidget(self.tabs)
        self.stack.addWidget(pagina_lista)

        # --- Página 1: Detalle ---
        self.pagina_detalle = QWidget()
        self.stack.addWidget(self.pagina_detalle)

        self.cargar_datos()

    def _crear_scroll(self):
        """Crea un QScrollArea con CSS para ocultar las barras cuadradas de Windows."""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        # Scrollbars modernas e invisibles hasta que se usan
        scroll.setStyleSheet("""
            QScrollArea { border: none; background: transparent; }
            QScrollBar:vertical {
                border: none;
                background: transparent;
                width: 8px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #CBD5E1;
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover { background: #94A3B8; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
        """)

        contenedor = QWidget()
        contenedor.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(contenedor)
        layout.setContentsMargins(5, 15, 15, 15)  # Margen derecho para que no pegue la tarjeta con la barra
        layout.setSpacing(15)
        layout.addStretch()

        scroll.setWidget(contenedor)
        return scroll

    def _limpiar_scroll(self, scroll):
        layout = scroll.widget().layout()
        while layout.count() > 1:
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def cargar_datos(self):
        self._limpiar_scroll(self.scroll_prospectos)
        self._limpiar_scroll(self.scroll_clientes)

        prospectos_data = self.db.obtener_prospectos(self.usuario_id, self.es_admin)

        for fila in prospectos_data:
            if self.es_admin:
                pid, nombre, telefono, vendedor, es_cliente = fila
                nombre_mostrar = f"{nombre} (Vendedor: {vendedor})"
            else:
                pid, nombre, telefono, es_cliente = fila
                nombre_mostrar = nombre

            # Obtenemos la información de la cita en lugar del checklist
            cita_info = self.db.obtener_cita(pid)

            tarjeta = TarjetaProspecto(pid, nombre_mostrar, telefono, cita_info)
            tarjeta.clicked.connect(self._abrir_detalle)

            if es_cliente:
                layout = self.scroll_clientes.widget().layout()
            else:
                layout = self.scroll_prospectos.widget().layout()

            layout.insertWidget(layout.count() - 1, tarjeta)


    def _abrir_detalle(self, prospecto_id):
        todos = self.db.obtener_prospectos(self.usuario_id, self.es_admin)
        nombre, telefono = "—", ""
        for fila in todos:
            if fila[0] == prospecto_id:
                nombre = fila[1]
                telefono = fila[2]
                break

        layout_viejo = self.pagina_detalle.layout()
        if layout_viejo:
            QWidget().setLayout(layout_viejo)

        detalle = DetalleProspecto(prospecto_id, nombre, telefono)
        detalle.cerrado.connect(self._volver_lista)

        nuevo_layout = QVBoxLayout(self.pagina_detalle)
        nuevo_layout.setContentsMargins(0, 0, 0, 0)
        nuevo_layout.addWidget(detalle)

        self.stack.setCurrentIndex(1)

    def _volver_lista(self):
        self.cargar_datos()
        self.stack.setCurrentIndex(0)

    def _abrir_formulario_nuevo(self):
        dialogo = DialogoNuevoProspecto(self)
        if dialogo.exec():
            nombre, telefono = dialogo.obtener_datos()
            # Ya no llamamos al checklist, solo agregamos a la BD y recargamos
            self.db.agregar_prospecto(nombre, telefono, self.usuario_id)
            self.cargar_datos()