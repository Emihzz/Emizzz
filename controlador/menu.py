# -*- coding: utf-8 -*-
import sys
import os
import subprocess
import pymysql
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QScrollArea, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor


# Forzar UTF-8 como codificación predeterminada en Windows
if sys.platform == "win32":
    os.environ["PYTHONIOENCODING"] = "utf-8"


def conectar_base_datos():
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='Emiz',
            database='NETO',
            cursorclass=pymysql.cursors.DictCursor
        )
        print("[OK] Conexion exitosa a la base de datos.")
        return connection
    except Exception as e:
        # Evitar problemas con emojis o caracteres Unicode en Windows
        mensaje_error = f"Error al conectar a la base de datos:\n{str(e)}"
        QMessageBox.critical(None, "Error", mensaje_error)
        return None


class MenuPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Punto de Venta NETO - Menú Principal")
        self.resize(800, 600)
        self.setMinimumSize(600, 400)

        # Estilo general
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f7fa;
            }
            QPushButton {
                font-size: 14px;
                font-weight: bold;
                padding: 15px;
                border-radius: 8px;
                border: 2px solid #d1d8e0;
                min-width: 200px;
                color: #2c3e50;
            }
            QPushButton:hover {
                background-color: #d1d8e0;
            }
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #2c3e50;
                padding: 10px;
            }
        """)

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Título
        titulo = QLabel("NETO")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: #3498db;
                padding: 15px;
                background-color: #ecf0f1;
                border-radius: 10px;
                border-bottom: 3px solid #3498db;
            }
        """)
        main_layout.addWidget(titulo)

        # Scroll area para los botones
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
            }
            QScrollBar:vertical {
                width: 10px;
                background: #f1f1f1;
            }
            QScrollBar::handle:vertical {
                background: #c1c1c1;
                min-height: 20px;
                border-radius: 5px;
            }
        """)

        container = QWidget()
        scroll.setWidget(container)

        buttons_layout = QVBoxLayout(container)
        buttons_layout.setSpacing(15)
        buttons_layout.setContentsMargins(10, 10, 10, 10)

        # Botón de Ventas (en la parte superior)
        btn_ventas = self.create_module_button("Ventas", "#e67e22", "ventas.py")
        buttons_layout.insertWidget(0, btn_ventas)  # Insertar al inicio

        # Botones para cada módulo
        modulos = [
            ("Clientes", "#3498db", "clientes.py"),
            ("Empleados", "#2ecc71", "empleados.py"),
            ("Proveedores", "#e74c3c", "proveedores.py"),
            ("Categorías", "#9b59b6", "categorias.py"),
            ("Configuración", "#f39c12", "configuracion.py"),
            ("Cajas", "#34495e", "cajas.py")
        ]

        for texto, color, archivo in modulos:
            btn = self.create_module_button(texto, color, archivo)
            buttons_layout.addWidget(btn)

        buttons_layout.addStretch()

        # Botón de salida
        btn_salir = QPushButton("Salir del Sistema")
        btn_salir.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                font-size: 16px;
                padding: 12px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        btn_salir.clicked.connect(self.close)
        main_layout.addWidget(btn_salir)

        main_layout.addWidget(scroll)

    def create_module_button(self, texto, color, archivo):
        btn = QPushButton(f"{texto}")
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                font-size: 16px;
                text-align: left;
                padding-left: 20px;
            }}
            QPushButton:hover {{
                background-color: {self.darken_color(color)};
                border: 2px solid {self.darken_color(color, 0.7)};
            }}
        """)
        btn.setFixedHeight(60)
        btn.clicked.connect(lambda checked, a=archivo: self.abrir_modulo(a))
        return btn

    def darken_color(self, hex_color, amount=0.8):
        color = QColor(hex_color.lstrip('#'))
        r, g, b = color.red(), color.green(), color.blue()
        r = int(r * amount)
        g = int(g * amount)
        b = int(b * amount)
        return f"#{r:02x}{g:02x}{b:02x}"

    def abrir_modulo(self, archivo):
        try:
            # Ruta base del proyecto (carpeta padre de 'controlador')
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            ruta_modulo = os.path.join(base_dir, "vista", archivo)

            if not os.path.exists(ruta_modulo):
                raise FileNotFoundError(f"No se encontró el archivo: {ruta_modulo}")

            # Ejecutar el módulo
            subprocess.Popen([sys.executable, ruta_modulo])
        except Exception as e:
            error_msg = QMessageBox()
            error_msg.setIcon(QMessageBox.Icon.Critical)
            error_msg.setWindowTitle("Error")
            error_msg.setText(f"No se pudo abrir el módulo: {archivo}")
            error_msg.setInformativeText(str(e))
            error_msg.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    # Conectar a la base de datos NETO
    conn = conectar_base_datos()
    if not conn:
        sys.exit(1)

    # Estilo adicional
    app.setStyleSheet("""
        QMessageBox {
            font-size: 14px;
        }
    """)

    ventana = MenuPrincipal()
    ventana.show()
    sys.exit(app.exec())