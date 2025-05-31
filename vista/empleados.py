# -*- coding: utf-8 -*-
import sys
import os

# Forzar UTF-8 en Windows
if sys.platform == "win32":
    os.environ["PYTHONIOENCODING"] = "utf-8"

from PyQt6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QScrollArea, QFrame, QWidget, QMainWindow
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
import pymysql


# Función de conexión a la base de datos con PyMySQL
def conectar_base_datos():
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='Emiz',  # Cambia esto por tu contraseña real
            database='NETO',
            cursorclass=pymysql.cursors.DictCursor
        )
        print("[OK] Conexión exitosa a la base de datos NETO.")
        return connection
    except Exception as e:
        mensaje_error = f"No se pudo conectar a la base de datos:\n{str(e)}"
        QMessageBox.critical(None, "Error", mensaje_error)
        return None


class VentanaDatos(QMainWindow):
    def __init__(self, datos_guardados):
        super().__init__()
        self.setWindowTitle("Datos Guardados - EMPLEADOS")
        self.resize(1200, 600)
        self.datos_guardados = datos_guardados
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Tabla de datos
        self.tabla_datos = QTableWidget()
        self.tabla_datos.setStyleSheet("""
            QTableWidget {
                font-size: 14px;
                border: none;
                alternate-background-color: #f8f9fa;
                color: #2c3e50;
            }
            QHeaderView::section {
                font-size: 14px;
                padding: 12px;
                background-color: #3498db;
                color: white;
                font-weight: bold;
                border: none;
            }
            QTableWidget::item {
                padding: 10px;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
        """)

        # Configuración de la tabla
        self.tabla_datos.setRowCount(0)
        self.tabla_datos.setColumnCount(14)
        self.tabla_datos.setHorizontalHeaderLabels([
            "ID Empleado", "Nombre", "Apellido Paterno", "Apellido Materno",
            "RFC", "CURP", "Dirección", "Teléfono", "Email",
            "Fecha Nacimiento", "Fecha Contratación", "Puesto", "Salario", "Activo"
        ])
        self.tabla_datos.verticalHeader().setDefaultSectionSize(40)
        self.tabla_datos.horizontalHeader().setStretchLastSection(True)
        self.tabla_datos.setAlternatingRowColors(True)
        self.tabla_datos.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        # Botón Eliminar
        btn_eliminar = QPushButton("Eliminar Registro Seleccionado")
        btn_eliminar.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                padding: 8px;
                font-size: 12px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        btn_eliminar.clicked.connect(self.eliminar_registro)

        # Organización del layout
        layout.addWidget(self.tabla_datos)
        layout.addWidget(btn_eliminar)
        self.mostrar_datos()

    def mostrar_datos(self):
        self.tabla_datos.setRowCount(len(self.datos_guardados))
        for row, empleado in enumerate(self.datos_guardados):
            for col, campo in enumerate(empleado.keys()):
                item = QTableWidgetItem(str(empleado[campo]))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.tabla_datos.setItem(row, col, item)
        self.tabla_datos.resizeColumnsToContents()

    def eliminar_registro(self):
        fila_seleccionada = self.tabla_datos.currentRow()
        if fila_seleccionada == -1:
            QMessageBox.warning(self, "Error", "Por favor seleccione un registro para eliminar")
            return
        respuesta = QMessageBox.question(
            self,
            "Confirmar Eliminación",
            "¿Está seguro que desea eliminar este registro?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if respuesta == QMessageBox.StandardButton.Yes:
            self.datos_guardados.pop(fila_seleccionada)
            self.mostrar_datos()
            QMessageBox.information(self, "Éxito", "Registro eliminado correctamente")


class FormularioEmpleados(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Formulario - EMPLEADOS")
        self.resize(1000, 600)
        self.setMinimumSize(800, 400)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowMinMaxButtonsHint)
        self.campos = ["id_empleado", "nombre", "apellido_paterno", "apellido_materno", "rfc",
                      "curp", "direccion", "telefono", "email", "fecha_nacimiento",
                      "fecha_contratacion", "puesto", "salario", "activo"]
        self.entradas = {}
        self.datos_guardados = []
        self.init_ui()

    def init_ui(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea { border: none; }
            QScrollBar:vertical { width: 10px; background: #f1f1f1; }
            QScrollBar::handle:vertical { background: #c1c1c1; min-height: 20px; border-radius: 5px; }
        """)

        container = QWidget()
        self.main_layout = QVBoxLayout(container)
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        self.main_layout.setSpacing(15)

        # Título más compacto
        titulo = QLabel("EMPLEADOS")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("""
            QLabel {
                font-size: 22px;
                font-weight: bold;
                color: #2c3e50;
                padding: 10px;
                background-color: #ecf0f1;
                border-radius: 5px;
                margin-bottom: 10px;
            }
        """)
        self.main_layout.addWidget(titulo)

        # Formulario
        self.setup_formulario()

        # Botones más pequeños
        self.setup_botones()

        scroll.setWidget(container)
        layout = QVBoxLayout(self)
        layout.addWidget(scroll)
        self.setLayout(layout)

    def setup_formulario(self):
        form_card = QFrame()
        form_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 6px;
                padding: 15px;
                border: 1px solid #dfe6e9;
                margin-bottom: 10px;
            }
        """)

        formulario_layout = QFormLayout()
        formulario_layout.setSpacing(10)
        formulario_layout.setContentsMargins(10, 10, 10, 10)

        font = QFont()
        font.setPointSize(11)
        font.setBold(True)

        for campo in self.campos:
            entrada = QLineEdit()
            entrada.setFont(QFont("Arial", 11))
            entrada.setMinimumHeight(35)
            entrada.setStyleSheet("""
                QLineEdit {
                    font-size: 12px;
                    padding: 8px;
                    border: 1px solid #bdc3c7;
                    border-radius: 4px;
                    color: #2c3e50;
                    background-color: #ffffff;
                }
                QLineEdit:focus {
                    border: 2px solid #3498db;
                }
            """)
            label = QLabel(f"{campo.replace('_', ' ').upper()}:")
            label.setFont(font)
            label.setStyleSheet("""
                font-weight: bold;
                color: #2c3e50;
                background-color: #ecf0f1;
                padding: 6px 10px;
                border-radius: 3px;
                border-left: 3px solid #3498db;
            """)
            formulario_layout.addRow(label, entrada)
            self.entradas[campo] = entrada

        form_card.setLayout(formulario_layout)
        self.main_layout.addWidget(form_card)

    def setup_botones(self):
        botones_layout = QHBoxLayout()
        botones_layout.setSpacing(10)

        botones = [
            ("Guardar", "#2ecc71", "💾", self.guardar_datos),
            ("Mostrar", "#f39c12", "👀", self.mostrar_ventana_datos),
            ("Limpiar", "#3498db", "🧹", self.limpiar_datos),
            ("Cerrar", "#7f8c8d", "✕", self.close)
        ]

        for texto, color, icono, funcion in botones:
            btn = QPushButton(f"{icono} {texto}")
            btn.setStyleSheet(f"""
                QPushButton {{
                    font-size: 12px;
                    font-weight: bold;
                    padding: 8px 12px;
                    border-radius: 4px;
                    background-color: {color};
                    color: white;
                    border: none;
                    min-width: 80px;
                }}
                QPushButton:hover {{
                    background-color: {self.darken_color(color)};
                }}
            """)
            btn.clicked.connect(funcion)
            botones_layout.addWidget(btn)

        self.main_layout.addLayout(botones_layout)

    def mostrar_ventana_datos(self):
        if not self.datos_guardados:
            QMessageBox.warning(self, "Advertencia", "No hay datos guardados para mostrar")
            return
        self.ventana_datos = VentanaDatos(self.datos_guardados)
        self.ventana_datos.show()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_F11:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()
        else:
            super().keyPressEvent(event)

    def darken_color(self, hex_color, amount=0.8):
        color = QColor(hex_color)
        return color.darker(int(100 + (100 * (1 - amount)))).name()

    def guardar_datos(self):
        conn = conectar_base_datos()
        if conn:
            try:
                with conn.cursor() as cursor:
                    # Obtener los valores del formulario
                    id_empleado = self.entradas["id_empleado"].text()
                    nombre = self.entradas["nombre"].text()
                    apellido_paterno = self.entradas["apellido_paterno"].text()
                    apellido_materno = self.entradas["apellido_materno"].text()
                    rfc = self.entradas["rfc"].text()
                    curp = self.entradas["curp"].text()
                    direccion = self.entradas["direccion"].text()
                    telefono = self.entradas["telefono"].text()
                    email = self.entradas["email"].text()
                    fecha_nacimiento = self.entradas["fecha_nacimiento"].text()
                    fecha_contratacion = self.entradas["fecha_contratacion"].text()
                    puesto = self.entradas["puesto"].text()
                    salario = self.entradas["salario"].text()
                    activo_texto = self.entradas["activo"].text().strip().lower()

                    # Validar campos obligatorios
                    if not id_empleado or not nombre or not apellido_paterno or not telefono:
                        QMessageBox.warning(self, "Error", "Campos obligatorios incompletos.")
                        return

                    # Validar campo 'activo'
                    if activo_texto not in ["sí", "no"]:
                        QMessageBox.warning(self, "Error", "El campo 'Activo' debe ser 'Sí' o 'No'.")
                        return

                    # Convertir Sí/No a booleano
                    activo = activo_texto == "sí"

                    # Insertar en la base de datos
                    sql = """
                        INSERT INTO empleados (
                            id_empleado, nombre, apellido_paterno, apellido_materno,
                            rfc, curp, direccion, telefono, email,
                            fecha_nacimiento, fecha_contratacion, puesto, salario, activo
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(sql, (
                        id_empleado, nombre, apellido_paterno, apellido_materno,
                        rfc, curp, direccion, telefono, email,
                        fecha_nacimiento, fecha_contratacion, puesto, float(salario), int(activo)
                    ))
                    conn.commit()

                    # Actualizar lista local
                    self.datos_guardados.append({
                        "id_empleado": id_empleado,
                        "nombre": nombre,
                        "apellido_paterno": apellido_paterno,
                        "apellido_materno": apellido_materno,
                        "rfc": rfc,
                        "curp": curp,
                        "direccion": direccion,
                        "telefono": telefono,
                        "email": email,
                        "fecha_nacimiento": fecha_nacimiento,
                        "fecha_contratacion": fecha_contratacion,
                        "puesto": puesto,
                        "salario": salario,
                        "activo": activo
                    })

                    QMessageBox.information(self, "Éxito", "Empleado guardado correctamente.")
                    self.limpiar_datos()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudieron guardar los datos:\n{e}")
            finally:
                conn.close()

    def limpiar_datos(self):
        for entrada in self.entradas.values():
            entrada.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    if not conectar_base_datos():
        sys.exit(1)

    ventana = FormularioEmpleados()
    ventana.show()
    sys.exit(app.exec())