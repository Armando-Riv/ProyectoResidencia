import sys
from PySide6.QtWidgets import QApplication
from database import GestorBD
from vistas import VentanaLogin

def main():
    # 1. Asegurarnos de que la base de datos existe
    db = GestorBD()
    db.inicializar_bd()

    # 2. Iniciar la aplicación de PySide6
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # 3. Mostrar el Login
    ventana_login = VentanaLogin()
    ventana_login.show()

    # 4. Ejecutar el ciclo de eventos
    sys.exit(app.exec())

if __name__ == "__main__":
    main()