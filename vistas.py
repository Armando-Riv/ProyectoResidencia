import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                               QPushButton, QFrame, QMessageBox, QGraphicsDropShadowEffect,QTableWidget, QTableWidgetItem, QHeaderView, QTabWidget,QProgressBar, QCheckBox, QScrollArea,
                                QStackedWidget, QSizePolicy)
from PySide6.QtGui import QPixmap, QIcon, QAction, QColor
from PySide6.QtCore import Qt, QSize
from database import GestorBD

from PySide6.QtCore import Qt, QSize, Signal


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


# -------------------------------------------------------
# WIDGET: Detalle de un prospecto con checklist visual
# -------------------------------------------------------
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
# PANEL PRINCIPAL — reemplaza PanelProspectos
# -------------------------------------------------------
class PanelProspectos(QWidget):
    """Dos pestañas: Mis Prospectos / Mis Clientes. Cada una con cards."""

    PASOS = ["Contacto inicial", "Medición", "Diseño enviado", "Cotización aceptada", "Cliente"]

    def __init__(self, usuario_info):
        super().__init__()
        self.usuario_id = usuario_info['id']
        self.es_admin = usuario_info['rol'] == 'admin'
        self.db = GestorBD()

        # Stack: página 0 = lista con pestañas, página 1 = detalle
        self.stack = QStackedWidget()
        layout_root = QVBoxLayout(self)
        layout_root.setContentsMargins(0, 0, 0, 0)
        layout_root.addWidget(self.stack)

        # --- Página 0: Lista ---
        pagina_lista = QWidget()
        layout_lista = QVBoxLayout(pagina_lista)
        layout_lista.setContentsMargins(10, 10, 10, 10)

        titulo = QLabel("Seguimiento de Prospectos y Clientes")
        titulo.setStyleSheet("font-size: 18px; font-weight: bold; color: #2C3E50; margin-bottom: 6px;")
        layout_lista.addWidget(titulo)

        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabBar::tab { height: 36px; width: 180px; font-weight: bold; }
            QTabBar::tab:selected { color: #EF7C0F; border-bottom: 2px solid #EF7C0F; }
        """)

        # Pestaña Prospectos
        self.scroll_prospectos = self._crear_scroll()
        self.tabs.addTab(self.scroll_prospectos, "⏳  Prospectos")

        # Pestaña Clientes
        self.scroll_clientes = self._crear_scroll()
        self.tabs.addTab(self.scroll_clientes, "✅  Clientes")

        layout_lista.addWidget(self.tabs)
        self.stack.addWidget(pagina_lista)

        # --- Página 1: Detalle (se crea dinámicamente) ---
        self.pagina_detalle = QWidget()
        self.stack.addWidget(self.pagina_detalle)

        self.cargar_datos()

    def _crear_scroll(self):
        """Crea un QScrollArea con un layout de cards vertical."""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        contenedor = QWidget()
        contenedor.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(contenedor)
        layout.setContentsMargins(4, 8, 4, 8)
        layout.setSpacing(10)
        layout.addStretch()

        scroll.setWidget(contenedor)
        return scroll

    def _limpiar_scroll(self, scroll):
        layout = scroll.widget().layout()
        while layout.count() > 1:  # Deja el stretch al final
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def cargar_datos(self):
        """Refresca ambas pestañas."""
        self._limpiar_scroll(self.scroll_prospectos)
        self._limpiar_scroll(self.scroll_clientes)

        prospectos_data = self.db.obtener_prospectos(self.usuario_id, self.es_admin)

        for fila in prospectos_data:
            if self.es_admin:
                pid, nombre, telefono, vendedor, es_cliente = fila
            else:
                pid, nombre, telefono, es_cliente = fila

            # Inicializar checklist si no existe y contar completados
            self.db.inicializar_checklist_prospecto(pid)
            checklist = self.db.obtener_checklist(pid)
            completados = sum(1 for _, _, c in checklist if c)

            tarjeta = TarjetaProspecto(pid, nombre, telefono, completados)
            tarjeta.clicked.connect(self._abrir_detalle)

            if es_cliente:
                layout = self.scroll_clientes.widget().layout()
            else:
                layout = self.scroll_prospectos.widget().layout()

            layout.insertWidget(layout.count() - 1, tarjeta)

    def _abrir_detalle(self, prospecto_id):
        """Muestra el panel de detalle para el prospecto seleccionado."""
        # Buscar nombre y teléfono
        todos = self.db.obtener_prospectos(self.usuario_id, self.es_admin)
        nombre, telefono = "—", ""
        for fila in todos:
            if fila[0] == prospecto_id:
                nombre = fila[1]
                telefono = fila[2]
                break

        # Reemplazar página de detalle
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
        self.cargar_datos()  # Refresca por si cambió algún paso
        self.stack.setCurrentIndex(0)