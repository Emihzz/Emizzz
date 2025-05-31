# -*- coding: utf-8 -*-
import sys
import os
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
                            QLabel, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem, 
                            QComboBox, QFrame, QMessageBox, QTextEdit, QScrollArea, QInputDialog)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor, QBrush
import pymysql

# ----------------------------
# CONEXIÓN A BASE DE DATOS
# ----------------------------
def conectar_base_datos():
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='Emiz',
            database='NETO',
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except Exception as e:
        QMessageBox.critical(None, "Error", f"No se pudo conectar a la base de datos:\n{str(e)}")
        return None

# ----------------------------
# VENTANA PRINCIPAL
# ----------------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Ventas - Menú Principal")
        self.resize(800, 500)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2c3e50;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 15px;
                font-size: 16px;
                border-radius: 5px;
                min-width: 200px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QLabel {
                color: #ecf0f1;
            }
        """)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)
        
        # Título
        titulo = QLabel("SISTEMA DE VENTAS")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("""
            QLabel {
                font-size: 28px; 
                font-weight: bold; 
                color: #f1c40f;
                margin-bottom: 40px;
                padding: 15px;
                background-color: #34495e;
                border-radius: 10px;
                border: 2px solid #f1c40f;
            }
        """)
        layout.addWidget(titulo)
        
        # Botones de navegación
        btn_clientes = QPushButton("👥 Gestión de Clientes")
        btn_clientes.setStyleSheet("""
            QPushButton {
                background-color: #16a085;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #1abc9c;
            }
        """)
        btn_clientes.clicked.connect(self.abrir_clientes)
        
        btn_ventas = QPushButton("💰 Registrar Ventas")
        btn_ventas.setStyleSheet("""
            QPushButton {
                background-color: #e67e22;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #d35400;
            }
        """)
        btn_ventas.clicked.connect(self.abrir_ventas)
        
        btn_inventario = QPushButton("📦 Control de Inventario")
        btn_inventario.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
        """)
        btn_inventario.clicked.connect(self.abrir_inventario)
        
        btn_salir = QPushButton("🚪 Salir del Sistema")
        btn_salir.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        btn_salir.clicked.connect(self.close)
        
        layout.addWidget(btn_clientes)
        layout.addWidget(btn_ventas)
        layout.addWidget(btn_inventario)
        layout.addStretch()
        layout.addWidget(btn_salir)
    
    def abrir_clientes(self):
        self.ventana_clientes = VentanaClientes()
        self.ventana_clientes.show()
    
    def abrir_ventas(self):
        self.ventana_ventas = VentanaVentas()
        self.ventana_ventas.show()
    
    def abrir_inventario(self):
        self.ventana_inventario = VentanaInventario()
        self.ventana_inventario.show()

# ----------------------------
# VENTANA DE VENTAS CON FACTURACIÓN
# ----------------------------
class VentanaVentas(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registro de Ventas")
        self.resize(1200, 800)  # Más grande
        self.articulos_venta = []
        self.cliente_actual = None
        self.articulo_seleccionado = None  # Para mostrar detalles
        self.cmb_caja = QComboBox()
        self.btn_elegir_caja = QPushButton("Elegir Caja")
        self.btn_abrir_caja = QPushButton("Abrir Caja")  # NUEVO BOTÓN
        self.caja_seleccionada = None
        self.init_ui()
        
    def init_ui(self):
        # --- NUEVO: Widget de contenido y scroll ---
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        
        # Estilo de fondo
        content_widget.setStyleSheet("""
            QWidget {
                background-color: #ecf0f1;
            }
        """)
        
        # Título
        titulo = QLabel("REGISTRO DE VENTAS")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: white;
                padding: 15px;
                background-color: #e74c3c;
                border-radius: 10px;
                margin-bottom: 20px;
                border: 2px solid #c0392b;
            }
        """)
        layout.addWidget(titulo)
        
        # Sección de cliente
        cliente_frame = QFrame()
        cliente_frame.setStyleSheet("""
            QFrame {
                background-color: #3498db;
                border-radius: 10px;
                padding: 15px;
                border: 2px solid #2980b9;
                margin-bottom: 15px;
            }
            QLabel {
                color: white;
                font-weight: bold;
            }
        """)
        cliente_layout = QHBoxLayout(cliente_frame)
        
        self.txt_cliente = QLineEdit()
        self.txt_cliente.setPlaceholderText("Teléfono del cliente")
        self.txt_cliente.setStyleSheet("""
            QLineEdit {
                font-size: 14px;
                padding: 10px;
                border: 2px solid #2980b9;
                border-radius: 5px;
                color: #2c3e50;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #2ecc71;
                background-color: #ffffff;
            }
        """)
        
        btn_buscar_cliente = QPushButton("🔍 Buscar Cliente")
        btn_buscar_cliente.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                font-weight: bold;
                padding: 10px 15px;
                border-radius: 5px;
                background-color: #2ecc71;
                color: white;
                border: none;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        btn_buscar_cliente.clicked.connect(self.buscar_cliente)
        
        self.lbl_info_cliente = QLabel("Cliente: GENERAL")
        self.lbl_info_cliente.setStyleSheet("""
            QLabel {
                font-size: 14px; 
                color: white;
                font-weight: bold;
                padding: 8px;
                background-color: #34495e;
                border-radius: 5px;
            }
        """)
        
        cliente_layout.addWidget(QLabel("Teléfono Cliente:"))
        cliente_layout.addWidget(self.txt_cliente)
        cliente_layout.addWidget(btn_buscar_cliente)
        cliente_layout.addWidget(self.lbl_info_cliente)
        cliente_layout.addStretch()
        
        layout.addWidget(cliente_frame)
        
        # Sección de artículo (más grande y con scroll para detalles)
        articulo_frame = QFrame()
        articulo_frame.setStyleSheet("""
            QFrame {
                background-color: #2ecc71;
                border-radius: 10px;
                padding: 15px;
                border: 2px solid #27ae60;
                margin-bottom: 15px;
            }
            QLabel {
                color: white;
                font-weight: bold;
            }
        """)
        articulo_layout = QHBoxLayout(articulo_frame)

        # Formulario de agregar artículo
        form_widget = QWidget()
        form_layout = QFormLayout(form_widget)
        self.txt_codigo = QLineEdit()
        self.txt_codigo.setPlaceholderText("Código de barras")
        self.txt_codigo.setStyleSheet("""
            QLineEdit {
                font-size: 14px;
                padding: 10px;
                border: 2px solid #27ae60;
                border-radius: 5px;
                color: #2c3e50;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
                background-color: #ffffff;
            }
        """)
        self.txt_cantidad = QLineEdit()
        self.txt_cantidad.setPlaceholderText("Cantidad")
        self.txt_cantidad.setStyleSheet("""
            QLineEdit {
                font-size: 14px;
                padding: 10px;
                border: 2px solid #27ae60;
                border-radius: 5px;
                color: #2c3e50;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
                background-color: #ffffff;
            }
        """)
        btn_agregar = QPushButton("➕ Agregar Artículo")
        btn_agregar.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                font-weight: bold;
                padding: 10px 15px;
                border-radius: 5px;
                background-color: #e67e22;
                color: white;
                border: none;
            }
            QPushButton:hover {
                background-color: #d35400;
            }
        """)
        btn_agregar.clicked.connect(self.agregar_articulo)
        form_layout.addRow("Código:", self.txt_codigo)
        form_layout.addRow("Cantidad:", self.txt_cantidad)
        form_layout.addRow(btn_agregar)

        # Detalles del artículo seleccionado (con scroll)
        self.detalle_articulo_area = QScrollArea()
        self.detalle_articulo_area.setWidgetResizable(True)
        self.detalle_articulo_widget = QWidget()
        self.detalle_articulo_layout = QVBoxLayout(self.detalle_articulo_widget)
        self.detalle_articulo_area.setWidget(self.detalle_articulo_widget)
        self.detalle_articulo_area.setMinimumWidth(350)
        self.detalle_articulo_area.setMinimumHeight(200)
        self.detalle_articulo_area.setMaximumHeight(300)

        # Inicialmente vacío
        self.mostrar_detalle_articulo(None)

        articulo_layout.addWidget(form_widget, 2)
        articulo_layout.addWidget(self.detalle_articulo_area, 3)
        layout.addWidget(articulo_frame)
        
        # Tabla de artículos (más grande y con scroll)
        self.tabla_articulos = QTableWidget()
        self.tabla_articulos.setStyleSheet("""
            QTableWidget {
                font-size: 14px;
                border: 2px solid #bdc3c7;
                alternate-background-color: #f8f9fa;
                color: #2c3e50;
                gridline-color: #bdc3c7;
                background-color: white;
                border-radius: 5px;
            }
            QHeaderView::section {
                font-size: 14px;
                padding: 12px;
                background-color: #9b59b6;
                color: white;
                font-weight: bold;
                border: none;
            }
            QTableWidget::item {
                padding: 10px;
                color: #2c3e50;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
        """)
        self.tabla_articulos.setColumnCount(7)
        self.tabla_articulos.setHorizontalHeaderLabels([
            "Código", "Descripción", "Cantidad", "Precio Unitario", "Importe", "Existencia", "Ver Detalle"
        ])
        self.tabla_articulos.verticalHeader().setDefaultSectionSize(40)
        self.tabla_articulos.horizontalHeader().setStretchLastSection(True)
        self.tabla_articulos.setAlternatingRowColors(True)
        self.tabla_articulos.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabla_articulos.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.tabla_articulos.setMinimumHeight(300)
        self.tabla_articulos.setMaximumHeight(400)
        self.tabla_articulos.cellClicked.connect(self.ver_detalle_articulo_tabla)

        btn_eliminar = QPushButton("❌ Eliminar Artículo Seleccionado")
        btn_eliminar.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        btn_eliminar.clicked.connect(self.eliminar_articulo)
        layout.addWidget(self.tabla_articulos)
        layout.addWidget(btn_eliminar)
        
        # Sección de totales y pago
        totales_frame = QFrame()
        totales_frame.setStyleSheet("""
            QFrame {
                background-color: #9b59b6;
                border-radius: 10px;
                padding: 15px;
                border: 2px solid #8e44ad;
                margin-bottom: 15px;
            }
            QLabel {
                color: white;
                font-weight: bold;
            }
        """)
        totales_layout = QFormLayout(totales_frame)
        
        self.lbl_subtotal = QLabel("$0.00")
        self.lbl_subtotal.setStyleSheet("""
            QLabel {
                font-size: 16px; 
                font-weight: bold; 
                color: #f1c40f;
                background-color: #34495e;
                padding: 5px;
                border-radius: 5px;
            }
        """)
        
        self.lbl_iva = QLabel("$0.00")
        self.lbl_iva.setStyleSheet("""
            QLabel {
                font-size: 16px; 
                font-weight: bold; 
                color: #f1c40f;
                background-color: #34495e;
                padding: 5px;
                border-radius: 5px;
            }
        """)
        
        self.lbl_total = QLabel("$0.00")
        self.lbl_total.setStyleSheet("""
            QLabel {
                font-size: 18px; 
                font-weight: bold; 
                color: #f1c40f;
                background-color: #2c3e50;
                padding: 5px;
                border-radius: 5px;
            }
        """)
        
        totales_layout.addRow("Subtotal:", self.lbl_subtotal)
        totales_layout.addRow("IVA (16%):", self.lbl_iva)
        totales_layout.addRow("TOTAL:", self.lbl_total)
        
        # Forma de pago
        self.cmb_forma_pago = QComboBox()
        self.cmb_forma_pago.addItems(["EFECTIVO", "TARJETA DE CRÉDITO", "TARJETA DE DÉBITO", "TRANSFERENCIA"])
        self.cmb_forma_pago.setStyleSheet("""
            QComboBox {
                font-size: 14px;
                padding: 8px;
                border: 2px solid #8e44ad;
                border-radius: 5px;
                color: #2c3e50;
                background-color: white;
            }
            QComboBox:focus {
                border: 2px solid #3498db;
                background-color: #ffffff;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                selection-background-color: #9b59b6;
                color: #2c3e50;
            }
        """)
        
        totales_layout.addRow("Forma de Pago:", self.cmb_forma_pago)
        
        # Efectivo recibido
        self.txt_efectivo = QLineEdit()
        self.txt_efectivo.setPlaceholderText("0.00")
        self.txt_efectivo.setStyleSheet("""
            QLineEdit {
                font-size: 14px;
                padding: 8px;
                border: 2px solid #8e44ad;
                border-radius: 5px;
                color: #2c3e50;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
                background-color: #ffffff;
            }
        """)
        totales_layout.addRow("Efectivo Recibido:", self.txt_efectivo)
        
        # Cambio
        self.lbl_cambio = QLabel("$0.00")
        self.lbl_cambio.setStyleSheet("""
            QLabel {
                font-size: 16px; 
                font-weight: bold; 
                color: #f1c40f;
                background-color: #34495e;
                padding: 5px;
                border-radius: 5px;
            }
        """)
        totales_layout.addRow("Cambio:", self.lbl_cambio)
        
        layout.addWidget(totales_frame)
        
        # Botones
        botones_frame = QFrame()
        botones_frame.setStyleSheet("""
            QFrame {
                background-color: #34495e;
                border-radius: 10px;
                padding: 10px;
                border: 2px solid #2c3e50;
            }
        """)
        botones_layout = QHBoxLayout(botones_frame)
        
        btn_pagar = QPushButton("💳 Realizar Pago")
        btn_pagar.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                font-weight: bold;
                padding: 12px 24px;
                border-radius: 5px;
                background-color: #27ae60;
                color: white;
                border: none;
            }
            QPushButton:hover {
                background-color: #219653;
            }
        """)
        btn_pagar.clicked.connect(self.realizar_pago)
        
        btn_factura = QPushButton("🧾 Generar Factura")
        btn_factura.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                font-weight: bold;
                padding: 12px 24px;
                border-radius: 5px;
                background-color: #3498db;
                color: white;
                border: none;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        btn_factura.clicked.connect(self.generar_factura)
        
        btn_limpiar = QPushButton("🧹 Limpiar Todo")
        btn_limpiar.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                font-weight: bold;
                padding: 12px 24px;
                border-radius: 5px;
                background-color: #e67e22;
                color: white;
                border: none;
            }
            QPushButton:hover {
                background-color: #d35400;
            }
        """)
        btn_limpiar.clicked.connect(self.limpiar_todo)
        
        btn_volver = QPushButton("✕ Volver al Menú")
        btn_volver.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                font-weight: bold;
                padding: 12px 24px;
                border-radius: 5px;
                background-color: #e74c3c;
                color: white;
                border: none;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        btn_volver.clicked.connect(self.close)
        
        botones_layout.addWidget(btn_pagar)
        botones_layout.addWidget(btn_factura)
        botones_layout.addWidget(btn_limpiar)
        botones_layout.addWidget(btn_volver)
        
        layout.addWidget(botones_frame)
        
        # --- FIN widgets y layouts ---

        # --- NUEVO: ScrollArea ---
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(content_widget)
        self.setCentralWidget(scroll)

        self.txt_efectivo.textChanged.connect(self.calcular_cambio)

        # Caja para elegir la caja de venta
        caja_frame = QFrame()
        caja_frame.setStyleSheet("""
            QFrame {
                background-color: #f1c40f;
                border-radius: 10px;
                padding: 10px;
                border: 2px solid #f39c12;
                margin-bottom: 10px;
            }
            QLabel {
                color: #2c3e50;
                font-weight: bold;
            }
        """)
        caja_layout = QHBoxLayout(caja_frame)
        caja_layout.addWidget(QLabel("Caja:"))
        self.cmb_caja.setStyleSheet("""
            QComboBox {
                font-size: 14px;
                padding: 8px;
                border: 2px solid #f39c12;
                border-radius: 5px;
                color: #2c3e50;
                background-color: white;
            }
        """)
        caja_layout.addWidget(self.cmb_caja)
        # Botón para elegir caja
        self.btn_elegir_caja.setStyleSheet("""
            QPushButton {
                background-color: #e67e22;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 8px 18px;
                border-radius: 5px;
                border: none;
            }
            QPushButton:hover {
                background-color: #d35400;
            }
        """)
        self.btn_elegir_caja.clicked.connect(self.elegir_caja)
        caja_layout.addWidget(self.btn_elegir_caja)
        # --- NUEVO: Botón Abrir Caja ---
        self.btn_abrir_caja.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 8px 18px;
                border-radius: 5px;
                border: none;
            }
            QPushButton:hover {
                background-color: #219653;
            }
        """)
        self.btn_abrir_caja.clicked.connect(self.abrir_caja)
        caja_layout.addWidget(self.btn_abrir_caja)
        # --- FIN NUEVO ---
        caja_layout.addStretch()
        layout.addWidget(caja_frame)
        self.cargar_cajas_disponibles()
        # --- FIN NUEVO ---

    def cargar_cajas_disponibles(self):
        conn = conectar_base_datos()
        self.cmb_caja.clear()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT id_caja, nombre FROM cajas WHERE activa = 1")
                    cajas = cursor.fetchall()
                    for caja in cajas:
                        self.cmb_caja.addItem(f"{caja['nombre']} (ID: {caja['id_caja']})", caja['id_caja'])
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudieron cargar las cajas:\n{e}")
            finally:
                conn.close()
        # Selecciona la primera caja por defecto
        if self.cmb_caja.count() > 0:
            self.cmb_caja.setCurrentIndex(0)
            self.caja_seleccionada = self.cmb_caja.currentData()
        else:
            self.caja_seleccionada = None

    def elegir_caja(self):
        # Guarda la caja seleccionada
        self.caja_seleccionada = self.cmb_caja.currentData()
        if self.caja_seleccionada:
            QMessageBox.information(self, "Caja seleccionada", f"Caja seleccionada: {self.cmb_caja.currentText()}")
        else:
            QMessageBox.warning(self, "Caja", "Debe seleccionar una caja activa.")

    def abrir_caja(self):
        id_caja = self.cmb_caja.currentData()
        if not id_caja:
            QMessageBox.warning(self, "Caja", "Debe seleccionar una caja activa.")
            return
        # Solicitar monto inicial al usuario
        monto_inicial, ok = QInputDialog.getDouble(
            self, "Monto Inicial", "Ingrese el monto inicial para la caja:", 0.0, 0, 9999999, 2
        )
        if not ok:
            return
        conn = conectar_base_datos()
        if not conn:
            return
        try:
            with conn.cursor() as cursor:
                # Obtener id_empleado (en un sistema real sería el usuario logueado)
                cursor.execute("SELECT id_empleado FROM empleados LIMIT 1")
                empleado = cursor.fetchone()
                id_empleado = empleado['id_empleado'] if empleado else 1
                # Verificar si ya hay una apertura activa
                cursor.execute("""
                    SELECT id_apertura FROM aperturascaja 
                    WHERE id_caja = %s AND id_empleado = %s AND fecha_hora_cierre IS NULL
                """, (id_caja, id_empleado))
                apertura = cursor.fetchone()
                if apertura:
                    QMessageBox.information(self, "Caja", "Ya existe una apertura activa para esta caja/empleado.")
                    return
                # Insertar nueva apertura con monto_inicial
                cursor.execute("""
                    INSERT INTO aperturascaja (id_caja, id_empleado, fecha_hora_apertura, monto_inicial)
                    VALUES (%s, %s, %s, %s)
                """, (id_caja, id_empleado, datetime.now(), monto_inicial))
                conn.commit()
                QMessageBox.information(self, "Caja", "Apertura de caja realizada correctamente.")
        except Exception as e:
            conn.rollback()
            QMessageBox.critical(self, "Error", f"No se pudo abrir la caja:\n{e}")
        finally:
            conn.close()

    def mostrar_detalle_articulo(self, articulo):
        # Limpia el layout
        for i in reversed(range(self.detalle_articulo_layout.count())):
            widget = self.detalle_articulo_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        if not articulo:
            label = QLabel("Selecciona un artículo para ver detalles.")
            label.setStyleSheet("color: #2c3e50; font-size: 15px;")
            self.detalle_articulo_layout.addWidget(label)
            return
        # Muestra todos los datos relevantes
        for key, value in articulo.items():
            label = QLabel(f"<b>{key.capitalize()}:</b> {value}")
            label.setStyleSheet("color: #2c3e50; font-size: 15px;")
            self.detalle_articulo_layout.addWidget(label)

    def ver_detalle_articulo_tabla(self, row, column):
        if row < 0 or row >= len(self.articulos_venta):
            self.mostrar_detalle_articulo(None)
            return
        articulo = self.articulos_venta[row]
        self.mostrar_detalle_articulo(articulo)

    def buscar_cliente(self):
        telefono = self.txt_cliente.text().strip()
        if not telefono:
            self.cliente_actual = None
            self.lbl_info_cliente.setText("Cliente: GENERAL")
            return
            
        conn = conectar_base_datos()
        if conn:
            try:
                with conn.cursor() as cursor:
                    sql = "SELECT * FROM clientes WHERE telefono = %s"
                    cursor.execute(sql, (telefono,))
                    cliente = cursor.fetchone()
                    
                    if cliente:
                        self.cliente_actual = cliente
                        nombre_completo = f"{cliente['nombre']} {cliente.get('apellido_paterno', '')} {cliente.get('apellido_materno', '')}"
                        self.lbl_info_cliente.setText(f"Cliente: {nombre_completo.strip()} (Puntos: {cliente['puntos_acumulados']})")
                    else:
                        self.cliente_actual = None
                        self.lbl_info_cliente.setText("Cliente: GENERAL")
                        QMessageBox.information(self, "Información", "Cliente no encontrado. Se registrará como venta general.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo buscar el cliente:\n{e}")
            finally:
                conn.close()
    
    def agregar_articulo(self):
        codigo = self.txt_codigo.text().strip()
        cantidad_texto = self.txt_cantidad.text().strip()
        
        if not codigo or not cantidad_texto:
            QMessageBox.warning(self, "Error", "Por favor ingrese el código y la cantidad del artículo")
            return
            
        try:
            cantidad = float(cantidad_texto)
            if cantidad <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Error", "La cantidad debe ser un número mayor que cero")
            return
            
        conn = conectar_base_datos()
        if conn:
            try:
                with conn.cursor() as cursor:
                    sql = """
                        SELECT a.*, p.precio_promocion 
                        FROM articulos a
                        LEFT JOIN promociones p ON a.codigo_barras = p.codigo_barras 
                            AND CURDATE() BETWEEN p.fecha_inicio AND p.fecha_fin 
                            AND p.activa = 1
                        WHERE a.codigo_barras = %s AND a.activo = 1
                    """
                    cursor.execute(sql, (codigo,))
                    articulo = cursor.fetchone()
                    
                    if not articulo:
                        QMessageBox.warning(self, "Error", "Artículo no encontrado o inactivo")
                        return
                    
                    # --- SOLUCIÓN: Convertir todos los valores Decimal a float antes de operar ---
                    precio = float(articulo['precio_promocion']) if articulo['precio_promocion'] else float(articulo['precio_venta'])
                    existencia = float(articulo['existencia'])
                    iva_valor = float(articulo['iva'])
                    
                    # Verificar existencia
                    if existencia < cantidad:
                        QMessageBox.warning(self, "Error", f"No hay suficiente existencia. Disponible: {existencia}")
                        return
                    
                    importe = precio * cantidad
                    iva = importe * iva_valor
                    
                    # Guardar todos los datos relevantes para mostrar en detalle
                    articulo_detalle = {
                        'codigo': codigo,
                        'nombre': articulo['nombre'],
                        'cantidad': cantidad,
                        'precio': precio,
                        'importe': importe,
                        'iva': iva,
                        'existencia': existencia,
                        'precio_compra': float(articulo['precio_compra']),
                        'categoria': articulo.get('id_categoria', ''),
                        'iva_tasa': iva_valor
                    }
                    self.articulos_venta.append(articulo_detalle)
                    self.actualizar_tabla_articulos()
                    self.txt_codigo.clear()
                    self.txt_cantidad.clear()
                    self.txt_codigo.setFocus()
                    
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo agregar el artículo:\n{e}")
            finally:
                conn.close()
    
    def actualizar_tabla_articulos(self):
        self.tabla_articulos.setRowCount(len(self.articulos_venta))
        
        subtotal = 0
        iva_total = 0
        
        for row, articulo in enumerate(self.articulos_venta):
            self.tabla_articulos.setItem(row, 0, QTableWidgetItem(str(articulo['codigo'])))
            self.tabla_articulos.setItem(row, 1, QTableWidgetItem(str(articulo['nombre'])))
            self.tabla_articulos.setItem(row, 2, QTableWidgetItem(str(articulo['cantidad'])))
            self.tabla_articulos.setItem(row, 3, QTableWidgetItem(f"${articulo['precio']:.2f}"))
            self.tabla_articulos.setItem(row, 4, QTableWidgetItem(f"${articulo['importe']:.2f}"))
            self.tabla_articulos.setItem(row, 5, QTableWidgetItem(str(articulo.get('existencia', ''))))
            # Botón para ver detalle
            btn_ver = QPushButton("Ver Detalle")
            btn_ver.setStyleSheet("""
                QPushButton {
                    background-color: #2980b9;
                    color: white;
                    font-size: 12px;
                    border-radius: 5px;
                    padding: 5px 10px;
                }
                QPushButton:hover {
                    background-color: #1abc9c;
                }
            """)
            btn_ver.clicked.connect(lambda _, r=row: self.mostrar_detalle_articulo(self.articulos_venta[r]))
            self.tabla_articulos.setCellWidget(row, 6, btn_ver)
            
            subtotal += articulo['importe']
            iva_total += articulo['iva']
        
        # Actualizar totales
        self.lbl_subtotal.setText(f"${subtotal:.2f}")
        self.lbl_iva.setText(f"${iva_total:.2f}")
        self.lbl_total.setText(f"${(subtotal + iva_total):.2f}")
        
        # Calcular cambio si hay efectivo recibido
        self.calcular_cambio()
    
    def eliminar_articulo(self):
        fila_seleccionada = self.tabla_articulos.currentRow()
        if fila_seleccionada == -1:
            QMessageBox.warning(self, "Error", "Por favor seleccione un artículo para eliminar")
            return
            
        respuesta = QMessageBox.question(
            self,
            "Confirmar Eliminación",
            "¿Está seguro que desea eliminar este artículo de la venta?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if respuesta == QMessageBox.StandardButton.Yes:
            self.articulos_venta.pop(fila_seleccionada)
            self.actualizar_tabla_articulos()
    
    def calcular_cambio(self):
        try:
            total_texto = self.lbl_total.text().replace("$", "")
            total = float(total_texto)
            
            efectivo_texto = self.txt_efectivo.text().strip()
            if not efectivo_texto:
                self.lbl_cambio.setText("$0.00")
                return
                
            efectivo = float(efectivo_texto)
            cambio = efectivo - total
            
            if cambio >= 0:
                self.lbl_cambio.setText(f"${cambio:.2f}")
            else:
                self.lbl_cambio.setText("$0.00")
        except ValueError:
            self.lbl_cambio.setText("$0.00")
    
    def realizar_pago(self):
        if not self.articulos_venta:
            QMessageBox.warning(self, "Error", "No hay artículos en la venta")
            return
            
        forma_pago = self.cmb_forma_pago.currentText()
        efectivo_texto = self.txt_efectivo.text().strip()
        
        if forma_pago == "EFECTIVO" and not efectivo_texto:
            QMessageBox.warning(self, "Error", "Para pago en efectivo debe ingresar el monto recibido")
            return
            
        try:
            total = float(self.lbl_total.text().replace("$", ""))
            
            if forma_pago == "EFECTIVO":
                efectivo = float(efectivo_texto)
                if efectivo < total:
                    QMessageBox.warning(self, "Error", "El efectivo recibido es menor que el total")
                    return
        except ValueError:
            QMessageBox.warning(self, "Error", "Monto inválido")
            return
            
        # Confirmar venta
        respuesta = QMessageBox.question(
            self,
            "Confirmar Venta",
            f"¿Confirmar venta por ${total:.2f}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if respuesta == QMessageBox.StandardButton.Yes:
            self.guardar_venta()
    
    def guardar_venta(self):
        conn = conectar_base_datos()
        if not conn:
            return
            
        try:
            with conn.cursor() as cursor:
                # Obtener datos necesarios
                total = float(self.lbl_total.text().replace("$", ""))
                subtotal = float(self.lbl_subtotal.text().replace("$", ""))
                iva = float(self.lbl_iva.text().replace("$", ""))
                forma_pago = self.cmb_forma_pago.currentText()
                efectivo = float(self.txt_efectivo.text()) if forma_pago == "EFECTIVO" else None
                cambio = float(self.lbl_cambio.text().replace("$", "")) if forma_pago == "EFECTIVO" else None
                
                # Obtener id_empleado (en un sistema real sería el usuario logueado)
                cursor.execute("SELECT id_empleado FROM empleados LIMIT 1")
                empleado = cursor.fetchone()
                id_empleado = empleado['id_empleado'] if empleado else 1

                # DEBUG: Mostrar id_caja y id_empleado antes de buscar apertura
                # print(f"DEBUG: id_caja={id_caja}, id_empleado={id_empleado}")

                # Obtener id_caja desde el combo o variable seleccionada
                id_caja = self.caja_seleccionada or self.cmb_caja.currentData()
                if not id_caja:
                    QMessageBox.warning(self, "Error", "Debe seleccionar una caja para la venta usando el botón 'Elegir Caja'")
                    return

                # Verificar si hay una apertura de caja activa
                cursor.execute("""
                    SELECT id_apertura FROM aperturascaja 
                    WHERE id_caja = %s AND id_empleado = %s AND fecha_hora_cierre IS NULL
                    ORDER BY fecha_hora_apertura DESC LIMIT 1
                """, (id_caja, id_empleado))
                apertura = cursor.fetchone()

                # --- AYUDA PARA EL USUARIO ---
                if not apertura:
                    # Mostrar información útil para depuración
                    cursor.execute("""
                        SELECT * FROM aperturascaja WHERE id_caja = %s AND id_empleado = %s
                        ORDER BY fecha_hora_apertura DESC LIMIT 1
                    """, (id_caja, id_empleado))
                    apertura_info = cursor.fetchone()
                    if not apertura_info:
                        QMessageBox.critical(
                            self, "Error",
                            f"No hay una apertura de caja activa para esta caja/empleado.\n\n"
                            f"¿Ya hiciste una apertura de caja para la caja seleccionada y el empleado {id_empleado}?\n"
                            f"Debes abrir caja antes de registrar ventas.\n"
                            f"Si no existe ninguna apertura para esta caja/empleado, crea una desde el módulo de cajas/aperturas."
                        )
                    else:
                        QMessageBox.critical(
                            self, "Error",
                            f"La última apertura de caja para esta caja/empleado ya está cerrada.\n"
                            f"Debes abrir una nueva caja antes de registrar ventas."
                        )
                    return
                
                id_apertura = apertura['id_apertura']
                telefono_cliente = self.cliente_actual['telefono'] if self.cliente_actual else None
                
                # Insertar venta
                sql_venta = """
                    INSERT INTO ventas (
                        id_apertura, telefono_cliente, fecha_hora, subtotal, 
                        iva, ieps, total, efectivo_recibido, cambio, forma_pago
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql_venta, (
                    id_apertura, telefono_cliente, datetime.now(), subtotal, 
                    iva, 0, total, efectivo, cambio, forma_pago
                ))
                id_venta = cursor.lastrowid
                
                # Insertar detalle de venta
                for articulo in self.articulos_venta:
                    sql_detalle = """
                        INSERT INTO detalleventa (
                            id_venta, codigo_barras, cantidad, precio_unitario, 
                            iva, ieps, importe
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(sql_detalle, (
                        id_venta, articulo['codigo'], articulo['cantidad'], 
                        articulo['precio'], articulo['iva'], 0, articulo['importe']
                    ))
                    
                    # Actualizar inventario
                    sql_inventario = """
                        INSERT INTO inventario (
                            codigo_barras, tipo_movimiento, cantidad, 
                            fecha_hora, id_referencia, tipo_referencia, 
                            motivo, id_empleado
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(sql_inventario, (
                        articulo['codigo'], 'VENTA', -articulo['cantidad'], 
                        datetime.now(), id_venta, 'VENTA', 
                        'Venta registrada', id_empleado
                    ))
                    
                    # Actualizar existencia en artículo
                    sql_update = """
                        UPDATE articulos 
                        SET existencia = existencia - %s 
                        WHERE codigo_barras = %s
                    """
                    cursor.execute(sql_update, (articulo['cantidad'], articulo['codigo']))
                
                # Si hay cliente, actualizar puntos
                if self.cliente_actual:
                    puntos = int(total) # 1 punto por cada $1 (ajustar según reglas de negocio)
                    sql_puntos = """
                        INSERT INTO puntosclientes (
                            telefono_cliente, id_venta, puntos, 
                            fecha_hora, tipo_movimiento
                        ) VALUES (%s, %s, %s, %s, %s)
                    """
                    cursor.execute(sql_puntos, (
                        telefono_cliente, id_venta, puntos, 
                        datetime.now(), 'ACUMULACION'
                    ))
                    
                    # Actualizar puntos acumulados en cliente
                    sql_update_cliente = """
                        UPDATE clientes 
                        SET puntos_acumulados = puntos_acumulados + %s 
                        WHERE telefono = %s
                    """
                    cursor.execute(sql_update_cliente, (puntos, telefono_cliente))
                
                conn.commit()
                QMessageBox.information(self, "Éxito", f"Venta registrada correctamente\nNúmero de venta: {id_venta}")
                self.generar_factura(id_venta)
                self.limpiar_todo()
                
        except Exception as e:
            conn.rollback()
            QMessageBox.critical(self, "Error", f"No se pudo registrar la venta:\n{e}")
        finally:
            conn.close()
    
    def generar_factura(self, id_venta=None):
        if not id_venta and not self.articulos_venta:
            QMessageBox.warning(self, "Error", "No hay artículos en la venta para generar factura")
            return
        
        # Crear ventana de factura
        self.ventana_factura = QMainWindow()
        self.ventana_factura.setWindowTitle("Factura de Venta")
        self.ventana_factura.resize(500, 700)
        self.ventana_factura.setStyleSheet("""
            QMainWindow {
                background-color: #ecf0f1;
            }
        """)
        
        central_widget = QWidget()
        self.ventana_factura.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Título
        titulo = QLabel("FACTURA DE VENTA")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("""
            QLabel {
                font-size: 22px;
                font-weight: bold;
                color: white;
                background-color: #e74c3c;
                padding: 15px;
                border-radius: 10px;
                margin-bottom: 15px;
                border: 2px solid #c0392b;
            }
        """)
        layout.addWidget(titulo)
        
        # Información de la venta
        info_venta = QLabel(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        info_venta.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #2c3e50;
                padding: 5px;
                background-color: #f1c40f;
                border-radius: 5px;
            }
        """)
        layout.addWidget(info_venta)
        
        if id_venta:
            info_venta.setText(info_venta.text() + f"\nN° Factura: {id_venta}")
        
        if self.cliente_actual:
            cliente_info = QLabel(f"Cliente: {self.cliente_actual['nombre']} {self.cliente_actual.get('apellido_paterno', '')}\n"
                                 f"Teléfono: {self.cliente_actual['telefono']}")
            cliente_info.setStyleSheet("""
                QLabel {
                    font-size: 14px;
                    color: #2c3e50;
                    padding: 5px;
                    background-color: #bdc3c7;
                    border-radius: 5px;
                }
            """)
            layout.addWidget(cliente_info)
        
        # Línea separadora
        separador = QFrame()
        separador.setFrameShape(QFrame.Shape.HLine)
        separador.setStyleSheet("""
            QFrame {
                color: #7f8c8d;
                border: 2px solid #7f8c8d;
            }
        """)
        layout.addWidget(separador)
        
        # Detalle de artículos
        detalle_label = QLabel("Detalle de Artículos:")
        detalle_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #2c3e50;
            }
        """)
        layout.addWidget(detalle_label)
        
        factura_text = QTextEdit()
        factura_text.setReadOnly(True)
        factura_text.setStyleSheet("""
            QTextEdit {
                font-family: 'Courier New', monospace;
                font-size: 14px;
                background-color: white;
                color: #2c3e50;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
            }
        """)
        
        # Encabezado de la tabla
        factura_text.append("CANT  DESCRIPCIÓN            PRECIO    IMPORTE")
        factura_text.append("-" * 50)
        
        # Agregar artículos
        for articulo in self.articulos_venta:
            linea = f"{articulo['cantidad']:>4}  {articulo['nombre'][:20]:<20}  ${articulo['precio']:>6.2f}  ${articulo['importe']:>7.2f}"
            factura_text.append(linea)
        
        # Totales
        factura_text.append("-" * 50)
        subtotal = float(self.lbl_subtotal.text().replace("$", ""))
        iva = float(self.lbl_iva.text().replace("$", ""))
        total = float(self.lbl_total.text().replace("$", ""))
        
        factura_text.append(f"{'SUBTOTAL:':>38} ${subtotal:>7.2f}")
        factura_text.append(f"{'IVA (16%):':>38} ${iva:>7.2f}")
        factura_text.append(f"{'TOTAL:':>38} ${total:>7.2f}")
        
        if self.cmb_forma_pago.currentText() == "EFECTIVO":
            efectivo = float(self.txt_efectivo.text())
            cambio = float(self.lbl_cambio.text().replace("$", ""))
            factura_text.append(f"{'EFECTIVO:':>38} ${efectivo:>7.2f}")
            factura_text.append(f"{'CAMBIO:':>38} ${cambio:>7.2f}")
        
        factura_text.append("\nGRACIAS POR SU COMPRA!")
        
        layout.addWidget(factura_text)
        
        # Botones
        btn_imprimir = QPushButton("🖨️ Imprimir Factura")
        btn_imprimir.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
                background-color: #3498db;
                color: white;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        btn_imprimir.clicked.connect(lambda: self.imprimir_factura(factura_text.toPlainText()))
        
        btn_cerrar = QPushButton("✕ Cerrar")
        btn_cerrar.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
                background-color: #e74c3c;
                color: white;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        btn_cerrar.clicked.connect(self.ventana_factura.close)
        
        botones_layout = QHBoxLayout()
        botones_layout.addWidget(btn_imprimir)
        botones_layout.addWidget(btn_cerrar)
        layout.addLayout(botones_layout)
        
        self.ventana_factura.show()
    
    def imprimir_factura(self, texto_factura):
        # En un sistema real, aquí iría el código para imprimir
        # Por ahora solo mostramos un mensaje
        QMessageBox.information(self, "Imprimir", "Factura enviada a impresora")
        print("=== FACTURA ===\n")
        print(texto_factura)
    
    def limpiar_todo(self):
        self.articulos_venta = []
        self.cliente_actual = None
        self.txt_cliente.clear()
        self.lbl_info_cliente.setText("Cliente: GENERAL")
        self.txt_codigo.clear()
        self.txt_cantidad.clear()
        self.txt_efectivo.clear()
        self.tabla_articulos.setRowCount(0)
        self.lbl_subtotal.setText("$0.00")
        self.lbl_iva.setText("$0.00")
        self.lbl_total.setText("$0.00")
        self.lbl_cambio.setText("$0.00")
        self.cmb_forma_pago.setCurrentIndex(0)

# ----------------------------
# VENTANA DE CLIENTES
# ----------------------------
class VentanaClientes(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Clientes")
        self.resize(1100, 600)
        self.init_ui()
    
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Estilo de fondo
        central_widget.setStyleSheet("""
            QWidget {
                background-color: #ecf0f1;
            }
        """)
        
        # Título
        titulo = QLabel("GESTIÓN DE CLIENTES")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: white;
                padding: 15px;
                background-color: #16a085;
                border-radius: 10px;
                margin-bottom: 20px;
                border: 2px solid #1abc9c;
            }
        """)
        layout.addWidget(titulo)
        
        # Sección de búsqueda
        busqueda_frame = QFrame()
        busqueda_frame.setStyleSheet("""
            QFrame {
                background-color: #1abc9c;
                padding: 15px;
                border-radius: 10px;
                border: 2px solid #16a085;
            }
            QLabel {
                color: white;
                font-weight: bold;
            }
        """)
        busqueda_layout = QHBoxLayout(busqueda_frame)
        
        self.txt_buscar_cliente = QLineEdit()
        self.txt_buscar_cliente.setPlaceholderText("Teléfono o nombre del cliente")
        self.txt_buscar_cliente.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #16a085;
                border-radius: 5px;
                font-size: 14px;
                background-color: white;
            }
        """)
        
        btn_buscar = QPushButton("🔍 Buscar")
        btn_buscar.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 5px;
                border: none;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        btn_buscar.clicked.connect(self.buscar_cliente)
        
        busqueda_layout.addWidget(QLabel("Buscar:"))
        busqueda_layout.addWidget(self.txt_buscar_cliente)
        busqueda_layout.addWidget(btn_buscar)
        
        layout.addWidget(busqueda_frame)
        
        # Tabla de clientes
        self.tabla_clientes = QTableWidget()
        self.tabla_clientes.setColumnCount(9)
        self.tabla_clientes.setHorizontalHeaderLabels([
            "Teléfono", "Nombre", "Apellido Paterno", "Apellido Materno",
            "Email", "Fecha Nacimiento", "Fecha Registro", "Puntos", "Acciones"
        ])
        self.tabla_clientes.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                font-size: 14px;
                alternate-background-color: #f8f9fa;
            }
            QHeaderView::section {
                background-color: #16a085;
                color: white;
                padding: 10px;
                font-weight: bold;
                border: none;
            }
            QTableWidget::item {
                padding: 8px;
            }
        """)
        layout.addWidget(self.tabla_clientes)
        
        # Botón volver
        btn_volver = QPushButton("← Volver al Menú Principal")
        btn_volver.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
                border: none;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        btn_volver.clicked.connect(self.close)
        layout.addWidget(btn_volver)
        
        # Cargar clientes
        self.cargar_clientes()

    def cargar_clientes(self):
        conn = conectar_base_datos()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM clientes WHERE activo = 1 LIMIT 50")
                    clientes = cursor.fetchall()
                    
                    self.tabla_clientes.setRowCount(len(clientes))
                    for row, cliente in enumerate(clientes):
                        item_tel = QTableWidgetItem(cliente['telefono'])
                        item_tel.setForeground(QBrush(QColor("#2c3e50")))
                        item_nom = QTableWidgetItem(cliente['nombre'])
                        item_nom.setForeground(QBrush(QColor("#2c3e50")))
                        item_ap = QTableWidgetItem(cliente.get('apellido_paterno', '') or '')
                        item_ap.setForeground(QBrush(QColor("#2c3e50")))
                        item_am = QTableWidgetItem(cliente.get('apellido_materno', '') or '')
                        item_am.setForeground(QBrush(QColor("#2c3e50")))
                        item_email = QTableWidgetItem(cliente.get('email', '') or '')
                        item_email.setForeground(QBrush(QColor("#2c3e50")))
                        item_fnac = QTableWidgetItem(str(cliente.get('fecha_nacimiento', '') or ''))
                        item_fnac.setForeground(QBrush(QColor("#2c3e50")))
                        item_freg = QTableWidgetItem(str(cliente.get('fecha_registro', '') or ''))
                        item_freg.setForeground(QBrush(QColor("#2c3e50")))
                        item_pts = QTableWidgetItem(str(cliente['puntos_acumulados']))
                        item_pts.setForeground(QBrush(QColor("#2c3e50")))
                        self.tabla_clientes.setItem(row, 0, item_tel)
                        self.tabla_clientes.setItem(row, 1, item_nom)
                        self.tabla_clientes.setItem(row, 2, item_ap)
                        self.tabla_clientes.setItem(row, 3, item_am)
                        self.tabla_clientes.setItem(row, 4, item_email)
                        self.tabla_clientes.setItem(row, 5, item_fnac)
                        self.tabla_clientes.setItem(row, 6, item_freg)
                        self.tabla_clientes.setItem(row, 7, item_pts)
                        btn_editar = QPushButton("✏️ Editar")
                        btn_editar.setStyleSheet("""
                            QPushButton {
                                background-color: #3498db;
                                color: white;
                                padding: 5px 10px;
                                border-radius: 5px;
                                font-size: 12px;
                                border: none;
                            }
                            QPushButton:hover {
                                background-color: #2980b9;
                            }
                        """)
                        self.tabla_clientes.setCellWidget(row, 8, btn_editar)
                        btn_editar.clicked.connect(lambda _, tel=cliente['telefono']: self.editar_cliente(tel))
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al cargar clientes:\n{e}")
            finally:
                conn.close()
    
    def buscar_cliente(self):
        termino = self.txt_buscar_cliente.text().strip()
        if not termino:
            self.cargar_clientes()
            return
            
        conn = conectar_base_datos()
        if conn:
            try:
                with conn.cursor() as cursor:
                    sql = """
                        SELECT * FROM clientes 
                        WHERE (telefono LIKE %s OR nombre LIKE %s 
                        OR apellido_paterno LIKE %s OR apellido_materno LIKE %s OR email LIKE %s)
                        AND activo = 1
                        LIMIT 50
                    """
                    param = f"%{termino}%"
                    cursor.execute(sql, (param, param, param, param, param))
                    clientes = cursor.fetchall()
                    
                    self.tabla_clientes.setRowCount(len(clientes))
                    for row, cliente in enumerate(clientes):
                        item_tel = QTableWidgetItem(cliente['telefono'])
                        item_tel.setForeground(QBrush(QColor("#2c3e50")))
                        item_nom = QTableWidgetItem(cliente['nombre'])
                        item_nom.setForeground(QBrush(QColor("#2c3e50")))
                        item_ap = QTableWidgetItem(cliente.get('apellido_paterno', '') or '')
                        item_ap.setForeground(QBrush(QColor("#2c3e50")))
                        item_am = QTableWidgetItem(cliente.get('apellido_materno', '') or '')
                        item_am.setForeground(QBrush(QColor("#2c3e50")))
                        item_email = QTableWidgetItem(cliente.get('email', '') or '')
                        item_email.setForeground(QBrush(QColor("#2c3e50")))
                        item_fnac = QTableWidgetItem(str(cliente.get('fecha_nacimiento', '') or ''))
                        item_fnac.setForeground(QBrush(QColor("#2c3e50")))
                        item_freg = QTableWidgetItem(str(cliente.get('fecha_registro', '') or ''))
                        item_freg.setForeground(QBrush(QColor("#2c3e50")))
                        item_pts = QTableWidgetItem(str(cliente['puntos_acumulados']))
                        item_pts.setForeground(QBrush(QColor("#2c3e50")))
                        self.tabla_clientes.setItem(row, 0, item_tel)
                        self.tabla_clientes.setItem(row, 1, item_nom)
                        self.tabla_clientes.setItem(row, 2, item_ap)
                        self.tabla_clientes.setItem(row, 3, item_am)
                        self.tabla_clientes.setItem(row, 4, item_email)
                        self.tabla_clientes.setItem(row, 5, item_fnac)
                        self.tabla_clientes.setItem(row, 6, item_freg)
                        self.tabla_clientes.setItem(row, 7, item_pts)
                        btn_editar = QPushButton("✏️ Editar")
                        btn_editar.setStyleSheet("""
                            QPushButton {
                                background-color: #3498db;
                                color: white;
                                padding: 5px 10px;
                                border-radius: 5px;
                                font-size: 12px;
                                border: none;
                            }
                            QPushButton:hover {
                                background-color: #2980b9;
                            }
                        """)
                        self.tabla_clientes.setCellWidget(row, 8, btn_editar)
                        btn_editar.clicked.connect(lambda _, tel=cliente['telefono']: self.editar_cliente(tel))
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al buscar clientes:\n{e}")
            finally:
                conn.close()
    
    def editar_cliente(self, telefono):
        conn = conectar_base_datos()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM clientes WHERE telefono = %s", (telefono,))
                    cliente = cursor.fetchone()
                    
                    if not cliente:
                        QMessageBox.warning(self, "Error", "Cliente no encontrado")
                        return
                    
                    self.ventana_editar_cliente = QMainWindow()
                    self.ventana_editar_cliente.setWindowTitle("Editar Cliente")
                    self.ventana_editar_cliente.resize(500, 500)
                    self.ventana_editar_cliente.setStyleSheet("""
                        QMainWindow {
                            background-color: #ecf0f1;
                        }
                    """)
                    
                    central_widget = QWidget()
                    self.ventana_editar_cliente.setCentralWidget(central_widget)
                    layout = QVBoxLayout(central_widget)
                    
                    # Título
                    titulo = QLabel("EDITAR CLIENTE")
                    titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    titulo.setStyleSheet("""
                        QLabel {
                            font-size: 20px;
                            font-weight: bold;
                            color: white;
                            background-color: #3498db;
                            padding: 15px;
                            border-radius: 10px;
                            margin-bottom: 20px;
                            border: 2px solid #2980b9;
                        }
                    """)
                    layout.addWidget(titulo)
                    
                    # Formulario
                    form_frame = QFrame()
                    form_frame.setStyleSheet("""
                        QFrame {
                            background-color: white;
                            border-radius: 10px;
                            padding: 20px;
                            border: 2px solid #bdc3c7;
                        }
                        QLabel {
                            font-weight: bold;
                            color: #2c3e50;
                        }
                    """)
                    form_layout = QFormLayout(form_frame)
                    
                    self.txt_edit_telefono = QLineEdit(cliente['telefono'])
                    self.txt_edit_nombre = QLineEdit(cliente['nombre'])
                    self.txt_edit_apellido_paterno = QLineEdit(cliente.get('apellido_paterno', ''))
                    self.txt_edit_apellido_materno = QLineEdit(cliente.get('apellido_materno', ''))
                    self.txt_edit_direccion = QLineEdit(cliente.get('direccion', ''))
                    self.txt_edit_email = QLineEdit(cliente.get('email', ''))
                    self.txt_edit_fecha_nacimiento = QLineEdit(str(cliente.get('fecha_nacimiento', '')))
                    
                    self.txt_edit_telefono.setReadOnly(True)
                    
                    for widget in [self.txt_edit_telefono, self.txt_edit_nombre, self.txt_edit_apellido_paterno, 
                                 self.txt_edit_apellido_materno, self.txt_edit_direccion, self.txt_edit_email, 
                                 self.txt_edit_fecha_nacimiento]:
                        widget.setStyleSheet("""
                            QLineEdit {
                                padding: 8px;
                                border: 2px solid #bdc3c7;
                                border-radius: 5px;
                                font-size: 14px;
                            }
                            QLineEdit:focus {
                                border: 2px solid #3498db;
                            }
                        """)
                    
                    form_layout.addRow("Teléfono:", self.txt_edit_telefono)
                    form_layout.addRow("Nombre:", self.txt_edit_nombre)
                    form_layout.addRow("Apellido Paterno:", self.txt_edit_apellido_paterno)
                    form_layout.addRow("Apellido Materno:", self.txt_edit_apellido_materno)
                    form_layout.addRow("Dirección:", self.txt_edit_direccion)
                    form_layout.addRow("Email:", self.txt_edit_email)
                    form_layout.addRow("Fecha Nacimiento:", self.txt_edit_fecha_nacimiento)
                    
                    layout.addWidget(form_frame)
                    
                    # Botones
                    btn_guardar = QPushButton("💾 Guardar Cambios")
                    btn_guardar.setStyleSheet("""
                        QPushButton {
                            background-color: #2ecc71;
                            color: white;
                            font-size: 16px;
                            font-weight: bold;
                            padding: 10px;
                            border-radius: 5px;
                            border: none;
                        }
                        QPushButton:hover {
                            background-color: #27ae60;
                        }
                    """)
                    btn_guardar.clicked.connect(lambda: self.actualizar_cliente(telefono))
                    
                    btn_cancelar = QPushButton("✕ Cancelar")
                    btn_cancelar.setStyleSheet("""
                        QPushButton {
                            background-color: #e74c3c;
                            color: white;
                            font-size: 16px;
                            font-weight: bold;
                            padding: 10px;
                            border-radius: 5px;
                            border: none;
                        }
                        QPushButton:hover {
                            background-color: #c0392b;
                        }
                    """)
                    btn_cancelar.clicked.connect(self.ventana_editar_cliente.close)
                    
                    botones_layout = QHBoxLayout()
                    botones_layout.addWidget(btn_guardar)
                    botones_layout.addWidget(btn_cancelar)
                    layout.addLayout(botones_layout)
                    
                    self.ventana_editar_cliente.show()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al cargar cliente:\n{e}")
            finally:
                conn.close()
    
    def actualizar_cliente(self, telefono_original):
        telefono = self.txt_edit_telefono.text().strip()
        nombre = self.txt_edit_nombre.text().strip()
        apellido_paterno = self.txt_edit_apellido_paterno.text().strip()
        apellido_materno = self.txt_edit_apellido_materno.text().strip()
        direccion = self.txt_edit_direccion.text().strip()
        email = self.txt_edit_email.text().strip()
        fecha_nacimiento = self.txt_edit_fecha_nacimiento.text().strip()
        
        try:
            puntos = int(self.txt_edit_puntos.text().strip())
        except ValueError:
            QMessageBox.warning(self.ventana_editar_cliente, "Error", "Los puntos deben ser un número entero")
            return
            
        if not nombre:
            QMessageBox.warning(self.ventana_editar_cliente, "Error", "El nombre es obligatorio")
            return
            
        conn = conectar_base_datos()
        if conn:
            try:
                with conn.cursor() as cursor:
                    # Verificar si el teléfono ha cambiado y si ya existe
                    if telefono != telefono_original:
                        cursor.execute("SELECT * FROM clientes WHERE telefono = %s", (telefono,))
                        if cursor.fetchone():
                            QMessageBox.warning(self.ventana_editar_cliente, "Error", "Ya existe un cliente con este nuevo teléfono")
                            return
                    
                    # Actualizar cliente
                    sql = """
                        UPDATE clientes SET
                            telefono = %s,
                            nombre = %s,
                            apellido_paterno = %s,
                            apellido_materno = %s,
                            direccion = %s,
                            email = %s,
                            fecha_nacimiento = %s,
                            puntos_acumulados = %s
                        WHERE telefono = %s
                    """
                    cursor.execute(sql, (
                        telefono, nombre, apellido_paterno, 
                        apellido_materno, direccion, email, fecha_nacimiento, puntos,
                        telefono_original
                    ))
                    conn.commit()
                    
                    QMessageBox.information(self.ventana_editar_cliente, "Éxito", "Cliente actualizado correctamente")
                    self.ventana_editar_cliente.close()
                    self.cargar_clientes()
            except Exception as e:
                conn.rollback()
                QMessageBox.critical(self.ventana_editar_cliente, "Error", f"No se pudo actualizar el cliente:\n{e}")
            finally:
                conn.close()

# ----------------------------
# VENTANA DE INVENTARIO
# ----------------------------
class VentanaInventario(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Control de Inventario")
        self.resize(1000, 600)
        self.init_ui()
    
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Estilo de fondo
        central_widget.setStyleSheet("""
            QWidget {
                background-color: #ecf0f1;
            }
        """)
        
        # Título
        titulo = QLabel("CONTROL DE INVENTARIO")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: white;
                background-color: #9b59b6;
                padding:   15px;
                border-radius: 10px;
                margin-bottom: 20px;
                border: 2px solid #8e44ad;
            }
        """)
        layout.addWidget(titulo)
        
        # Controles de búsqueda y filtrado
        filtros_frame = QFrame()
        filtros_frame.setStyleSheet("""
            QFrame {
                background-color: #8e44ad;
                padding: 15px;
                border-radius: 10px;
                border: 2px solid #9b59b6;
            }
            QLabel {
                color: white;
                font-weight: bold;
            }
        """)
        filtros_layout = QHBoxLayout(filtros_frame)

        self.txt_buscar_articulo = QLineEdit()
        self.txt_buscar_articulo.setPlaceholderText("Buscar por código o descripción")
        self.txt_buscar_articulo.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #9b59b6;
                border-radius: 5px;
                font-size: 14px;
                background-color: white;
            }
        """)

        btn_buscar = QPushButton("🔍 Buscar")
        btn_buscar.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 5px;
                border: none;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        btn_buscar.clicked.connect(self.buscar_articulos)

        filtros_layout.addWidget(QLabel("Buscar:"))
        filtros_layout.addWidget(self.txt_buscar_articulo)
        filtros_layout.addWidget(btn_buscar)
        # No botón de agregar artículo

        layout.addWidget(filtros_frame)
        
        # Tabla de inventario
        self.tabla_inventario = QTableWidget()
        self.tabla_inventario.setColumnCount(6)
        self.tabla_inventario.setHorizontalHeaderLabels([
            "Código", "Descripción", "Existencia", "Precio Compra", "Precio Venta", "Acciones"
        ])
        self.tabla_inventario.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                font-size: 14px;
                alternate-background-color: #f8f9fa;
            }
            QHeaderView::section {
                background-color: #9b59b6;
                color: white;
                padding: 10px;
                font-weight: bold;
                border: none;
            }
            QTableWidget::item {
                padding: 8px;
            }
        """)
        layout.addWidget(self.tabla_inventario)
        
        # Botón volver
        btn_volver = QPushButton("← Volver al Menú Principal")
        btn_volver.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
                border: none;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        btn_volver.clicked.connect(self.close)
        layout.addWidget(btn_volver)
        
        # Cargar inventario
        self.cargar_inventario()
    
    def cargar_inventario(self):
        conn = conectar_base_datos()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM articulos WHERE activo = 1 LIMIT 100")
                    articulos = cursor.fetchall()
                    
                    self.tabla_inventario.setRowCount(len(articulos))
                    for row, articulo in enumerate(articulos):

                        item_codigo = QTableWidgetItem(articulo['codigo_barras'])
                        item_codigo.setForeground(QBrush(QColor("#2c3e50")))
                        item_nombre = QTableWidgetItem(articulo['nombre'])
                        item_nombre.setForeground(QBrush(QColor("#2c3e50")))
                        item_exist = QTableWidgetItem(str(articulo['existencia']))
                        item_exist.setForeground(QBrush(QColor("#2c3e50")))
                        item_precio_compra = QTableWidgetItem(f"${articulo['precio_compra']:.2f}")
                        item_precio_compra.setForeground(QBrush(QColor("#2c3e50")))
                        item_precio_venta = QTableWidgetItem(f"${articulo['precio_venta']:.2f}")
                        item_precio_venta.setForeground(QBrush(QColor("#2c3e50")))
                        self.tabla_inventario.setItem(row, 0, item_codigo)
                        self.tabla_inventario.setItem(row, 1, item_nombre)
                        self.tabla_inventario.setItem(row, 2, item_exist)
                        self.tabla_inventario.setItem(row, 3, item_precio_compra)
                        self.tabla_inventario.setItem(row, 4, item_precio_venta)
                        # Botón editar
                        btn_editar = QPushButton("✏️ Editar")
                        btn_editar.setStyleSheet("""
                            QPushButton {
                                background-color: #3498db;
                                color: white;
                                padding: 5px 10px;
                                border-radius: 5px;
                                font-size: 12px;
                                border: none;
                            }
                            QPushButton:hover {
                                background-color: #2980b9;
                            }
                        """)
                        self.tabla_inventario.setCellWidget(row, 5, btn_editar)
                        btn_editar.clicked.connect(lambda _, cod=articulo['codigo_barras']: self.editar_articulo(cod))
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al cargar inventario:\n{e}")
            finally:
                conn.close()
    
    def buscar_articulos(self):
        termino = self.txt_buscar_articulo.text().strip()

        if not termino:
            self.cargar_inventario()
            return
            
        conn = conectar_base_datos()
        if conn:
            try:
                with conn.cursor() as cursor:
                    sql = """
                       
                       
                        SELECT * FROM articulos 
                        WHERE (codigo_barras LIKE %s OR nombre LIKE %s) 
                        AND activo = 1
                        LIMIT 100
                    """
                    param = f"%{termino}%"
                    cursor.execute(sql, (param, param))
                    articulos = cursor.fetchall()
                    
                    self.tabla_inventario.setRowCount(len(articulos))
                    for row, articulo in enumerate(articulos):
                        item_codigo = QTableWidgetItem(articulo['codigo_barras'])
                        item_codigo.setForeground(QBrush(QColor("#2c3e50")))
                        item_nombre = QTableWidgetItem(articulo['nombre'])
                        item_nombre.setForeground(QBrush(QColor("#2c3e50")))
                        item_exist = QTableWidgetItem(str(articulo['existencia']))
                        item_exist.setForeground(QBrush(QColor("#2c3e50")))
                        item_precio_compra = QTableWidgetItem(f"${articulo['precio_compra']:.2f}")
                        item_precio_compra.setForeground(QBrush(QColor("#2c3e50")))
                        item_precio_venta = QTableWidgetItem(f"${articulo['precio_venta']:.2f}")
                        item_precio_venta.setForeground(QBrush(QColor("#2c3e50")))
                        self.tabla_inventario.setItem(row, 0, item_codigo)
                        self.tabla_inventario.setItem(row, 1, item_nombre)
                        self.tabla_inventario.setItem(row, 2, item_exist)
                        self.tabla_inventario.setItem(row, 3, item_precio_compra)
                        self.tabla_inventario.setItem(row, 4, item_precio_venta)
                        # Botón editar
                        btn_editar = QPushButton("✏️ Editar")
                        btn_editar.setStyleSheet("""
                            QPushButton {
                                background-color: #3498db;
                                color: white;
                                padding: 5px 10px;
                                border-radius: 5px;
                                font-size: 12px;
                                border: none;
                            }
                            QPushButton:hover {
                                background-color: #2980b9;
                            }
                        """)
                        self.tabla_inventario.setCellWidget(row, 5, btn_editar)
                        btn_editar.clicked.connect(lambda _, cod=articulo['codigo_barras']: self.editar_articulo(cod))
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al buscar artículos:\n{e}")
            finally:
                conn.close()
    
    def editar_articulo(self, codigo):
        conn = conectar_base_datos()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM articulos WHERE codigo_barras = %s", (codigo,))
                    articulo = cursor.fetchone()
                    
                    if not articulo:
                        QMessageBox.warning(self, "Error", "Artículo no encontrado")
                        return
                    
                    self.ventana_editar_articulo = QMainWindow()
                    self.ventana_editar_articulo.setWindowTitle("Editar Artículo")
                    self.ventana_editar_articulo.resize(500, 500)
                    self.ventana_editar_articulo.setStyleSheet("""
                        QMainWindow {
                            background-color: #ecf0f1;
                        }
                    """)
                    
                    central_widget = QWidget()
                    self.ventana_editar_articulo.setCentralWidget(central_widget)
                    layout = QVBoxLayout(central_widget)
                    
                    # Título
                    titulo = QLabel("EDITAR ARTÍCULO")
                    titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    titulo.setStyleSheet("""
                        QLabel {
                            font-size: 20px;
                            font-weight: bold;
                            color: white;
                            background-color: #3498db;
                            padding: 15px;
                            border-radius: 10px;
                            margin-bottom:  20px;
                            border: 2px solid #2980b9;
                        }
                    """)
                    layout.addWidget(titulo)
                    
                    # Formulario
                    form_frame = QFrame()
                    form_frame.setStyleSheet("""
                        QFrame {
                            background-color: white;
                            border-radius: 10px;
                            padding: 20px;
                            border: 2px solid #bdc3c7;
                        }
                        QLabel {
                            font-weight: bold;
                            color: #2c3e50;
                        }
                    """)
                    form_layout = QFormLayout(form_frame)
                    
                    self.txt_edit_codigo = QLineEdit(articulo['codigo_barras'])
                    self.txt_edit_nombre = QLineEdit(articulo['nombre'])
                    self.txt_edit_existencia = QLineEdit(str(articulo['existencia']))
                    self.txt_edit_precio_compra = QLineEdit(str(articulo['precio_compra']))
                    self.txt_edit_precio_venta = QLineEdit(str(articulo['precio_venta']))
                    self.cmb_edit_iva = QComboBox()
                    self.cmb_edit_iva.addItems(["0.00", "0.16"])
                    self.cmb_edit_iva.setCurrentText(str(articulo['iva']))
                    
                    self.txt_edit_codigo.setReadOnly(True)
                    
                    for widget in [self.txt_edit_codigo, self.txt_edit_nombre, self.txt_edit_existencia, 
                                 self.txt_edit_precio_compra, self.txt_edit_precio_venta]:
                        widget.setStyleSheet("""
                            QLineEdit {
                                padding: 8px;
                                border: 2px solid #bdc3c7;
                                border-radius: 5px;
                                font-size: 14px;
                            }
                            QLineEdit:focus {
                                border: 2px solid #3498db;
                            }
                        """)
                    
                    self.cmb_edit_iva.setStyleSheet("""
                        QComboBox {
                            padding: 8px;
                            border: 2px solid #bdc3c7;
                            border-radius: 5px;
                            font-size: 14px;
                        }
                    """)
                    
                    form_layout.addRow("Código de Barras:", self.txt_edit_codigo)
                    form_layout.addRow("Nombre:", self.txt_edit_nombre)
                    form_layout.addRow("Existencia:", self.txt_edit_existencia)
                    form_layout.addRow("Precio Compra:", self.txt_edit_precio_compra)
                    form_layout.addRow("Precio Venta:", self.txt_edit_precio_venta)
                    form_layout.addRow("IVA:", self.cmb_edit_iva)
                    
                    layout.addWidget(form_frame)
                    
                    # Botones
                    btn_guardar = QPushButton("💾 Guardar Cambios")
                    btn_guardar.setStyleSheet("""
                        QPushButton {
                            background-color: #2ecc71;
                            color: white;
                            font-size: 16px;
                            font-weight: bold;
                            padding: 10px;
                            border-radius: 5px;
                            border: none;
                        }
                        QPushButton:hover {
                            background-color: #27ae60;
                        }
                    """)
                    btn_guardar.clicked.connect(lambda: self.actualizar_articulo(codigo))
                    
                    btn_cancelar = QPushButton("✕ Cancelar")
                    btn_cancelar.setStyleSheet("""
                        QPushButton {
                            background-color: #e74c3c;
                            color: white;
                            font-size: 16px;
                            font-weight: bold;
                            padding: 10px;
                            border-radius: 5px;
                            border: none;
                        }
                        QPushButton:hover {
                            background-color: #c0392b;
                        }
                    """)
                    btn_cancelar.clicked.connect(self.ventana_editar_articulo.close)
                    
                    botones_layout = QHBoxLayout()
                    botones_layout.addWidget(btn_guardar)
                    botones_layout.addWidget(btn_cancelar)
                    layout.addLayout(botones_layout)
                    
                    self.ventana_editar_articulo.show()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al cargar artículo:\n{e}")
            finally:
                conn.close()
    
    def actualizar_articulo(self, codigo_original):
        codigo = self.txt_edit_codigo.text().strip()
        nombre = self.txt_edit_nombre.text().strip()
        existencia_texto = self.txt_edit_existencia.text().strip()
        precio_compra_texto = self.txt_edit_precio_compra.text().strip()
        precio_venta_texto = self.txt_edit_precio_venta.text().strip()
        iva_texto = self.cmb_edit_iva.currentText()
        
        if not nombre:
            QMessageBox.warning(self.ventana_editar_articulo, "Error", "El nombre es obligatorio")
            return
            
        try:
            existencia = float(existencia_texto)
            precio_compra = float(precio_compra_texto)
            precio_venta = float(precio_venta_texto)
            iva = float(iva_texto)
            
            if existencia < 0 or precio_compra < 0 or precio_venta < 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self.ventana_editar_articulo, "Error", "Los valores numéricos deben ser positivos")
            return
            
        conn = conectar_base_datos()
        if conn:
            try:
                with conn.cursor() as cursor:
                    # Verificar si el código ha cambiado y si ya existe
                    if codigo != codigo_original:
                        cursor.execute("SELECT * FROM articulos WHERE codigo_barras = %s", (codigo,))
                        if cursor.fetchone():
                            QMessageBox.warning(self.ventana_editar_articulo, "Error", "Ya existe un artículo con este nuevo código")
                            return
                    
                    # Obtener existencia anterior para registrar diferencia
                    cursor.execute("SELECT existencia FROM articulos WHERE codigo_barras = %s", (codigo_original,))
                    existencia_anterior = cursor.fetchone()['existencia']
                    diferencia = existencia - existencia_anterior
                    
                    # Actualizar artículo
                    sql = """
                        UPDATE articulos SET
                            codigo_barras = %s,
                            nombre = %s,
                            existencia = %s,
                            precio_compra = %s,
                            precio_venta = %s,
                            iva = %s
                        WHERE codigo_barras = %s
                    """
                    cursor.execute(sql, (
                        codigo, nombre, existencia, 
                        precio_compra, precio_venta, iva,
                        codigo_original
                    ))
                    
                    # Registrar movimiento de inventario si hay diferencia
                    if diferencia != 0:
                        id_empleado = 1  # En un sistema real sería el usuario logueado
                        tipo_movimiento = 'ENTRADA' if diferencia > 0 else 'SALIDA'
                        sql_movimiento = """
                            INSERT INTO inventario (
                                codigo_barras, tipo_movimiento, cantidad, 
                                fecha_hora, id_referencia, tipo_referencia, 
                                motivo, id_empleado
                            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        """
                        cursor.execute(sql_movimiento, (
                            codigo, tipo_movimiento, abs(diferencia), 
                            datetime.now(), cursor.lastrowid, 'AJUSTE', 
                            'Ajuste de inventario', id_empleado
                        ))
                    
                    conn.commit()
                    
                    QMessageBox.information(self.ventana_editar_articulo, "Éxito", "Artículo actualizado correctamente")
                    self.ventana_editar_articulo.close()
                    self.cargar_inventario()
            except Exception as e:
                conn.rollback()
                QMessageBox.critical(self.ventana_editar_articulo, "Error", f"No se pudo actualizar el artículo:\n{e}")
            finally:
                conn.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())