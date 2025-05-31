CREATE DATABASE  NETO;
USE NETO;

CREATE TABLE Categorias (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    descripcion VARCHAR(100),
    activa BOOLEAN DEFAULT TRUE
);

CREATE TABLE Proveedores (
    id_proveedor INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    rfc CHAR(13),
    direccion VARCHAR(200),
    telefono CHAR(10) NOT NULL,
    email VARCHAR(100),
    activo BOOLEAN DEFAULT TRUE
);

CREATE TABLE Articulos (
    codigo_barras VARCHAR(20) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    id_categoria INT NOT NULL,
    id_proveedor INT,
    precio_venta DECIMAL(10,2) NOT NULL,
    precio_compra DECIMAL(10,2) NOT NULL,
    existencia DECIMAL(10,3) NOT NULL DEFAULT 0,
    unidad_medida VARCHAR(10) NOT NULL,
    iva DECIMAL(5,2) DEFAULT 0.16,
    ieps DECIMAL(5,2) DEFAULT 0,
    activo BOOLEAN DEFAULT TRUE,
    fecha_caducidad DATE,
    stock_minimo DECIMAL(10,3) DEFAULT 0,
    FOREIGN KEY (id_categoria) REFERENCES Categorias(id_categoria) ON UPDATE CASCADE,
    FOREIGN KEY (id_proveedor) REFERENCES Proveedores(id_proveedor) ON UPDATE CASCADE
);

CREATE TABLE Empleados (
    id_empleado INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido_paterno VARCHAR(50) NOT NULL,
    apellido_materno VARCHAR(50),
    rfc CHAR(13) NOT NULL,
    curp CHAR(18) NOT NULL,
    direccion VARCHAR(200),
    telefono CHAR(10) NOT NULL,
    email VARCHAR(100),
    fecha_nacimiento DATE NOT NULL,
    fecha_contratacion DATE NOT NULL,
    puesto VARCHAR(50) NOT NULL,
    salario DECIMAL(10,2) NOT NULL,
    activo BOOLEAN DEFAULT TRUE
);

CREATE TABLE Horarios (
    id_horario INT AUTO_INCREMENT PRIMARY KEY,
    id_empleado INT NOT NULL,
    dia_semana TINYINT NOT NULL,
    hora_entrada TIME NOT NULL,
    hora_salida TIME NOT NULL,
    FOREIGN KEY (id_empleado) REFERENCES Empleados(id_empleado) ON DELETE CASCADE
);

CREATE TABLE Clientes (
    telefono CHAR(10) PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido_paterno VARCHAR(50),
    apellido_materno VARCHAR(50),
    email VARCHAR(100),
    fecha_nacimiento DATE,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    puntos_acumulados INT DEFAULT 0,
    activo BOOLEAN DEFAULT TRUE
);

CREATE TABLE Cajas (
    id_caja INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    ubicacion VARCHAR(100) NOT NULL,
    activa BOOLEAN DEFAULT TRUE
);

CREATE TABLE AperturasCaja (
    id_apertura INT AUTO_INCREMENT PRIMARY KEY,
    id_caja INT NOT NULL,
    id_empleado INT NOT NULL,
    fecha_hora_apertura DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_hora_cierre DATETIME,
    monto_inicial DECIMAL(10,2) NOT NULL,
    monto_final DECIMAL(10,2),
    FOREIGN KEY (id_caja) REFERENCES Cajas(id_caja) ON UPDATE CASCADE,
    FOREIGN KEY (id_empleado) REFERENCES Empleados(id_empleado) ON UPDATE CASCADE
);

CREATE TABLE Ventas (
    id_venta INT AUTO_INCREMENT PRIMARY KEY,
    id_apertura INT NOT NULL,
    telefono_cliente CHAR(10),
    fecha_hora DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    subtotal DECIMAL(10,2) NOT NULL,
    iva DECIMAL(10,2) NOT NULL,
    ieps DECIMAL(10,2) NOT NULL DEFAULT 0,
    total DECIMAL(10,2) NOT NULL,
    efectivo_recibido DECIMAL(10,2),
    cambio DECIMAL(10,2),
    forma_pago VARCHAR(20) NOT NULL,
    cancelada BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (id_apertura) REFERENCES AperturasCaja(id_apertura) ON UPDATE CASCADE,
    FOREIGN KEY (telefono_cliente) REFERENCES Clientes(telefono) ON UPDATE CASCADE
);

CREATE TABLE DetalleVenta (
    id_detalle INT AUTO_INCREMENT PRIMARY KEY,
    id_venta INT NOT NULL,
    codigo_barras VARCHAR(20) NOT NULL,
    cantidad DECIMAL(10,3) NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    iva DECIMAL(10,2) NOT NULL,
    ieps DECIMAL(10,2) DEFAULT 0,
    importe DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_venta) REFERENCES Ventas(id_venta) ON DELETE CASCADE,
    FOREIGN KEY (codigo_barras) REFERENCES Articulos(codigo_barras) ON UPDATE CASCADE
);

CREATE TABLE Compras (
    id_compra INT AUTO_INCREMENT PRIMARY KEY,
    id_proveedor INT NOT NULL,
    id_empleado INT NOT NULL,
    fecha_hora DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    subtotal DECIMAL(10,2) NOT NULL,
    iva DECIMAL(10,2) NOT NULL,
    ieps DECIMAL(10,2) DEFAULT 0,
    total DECIMAL(10,2) NOT NULL,
    forma_pago VARCHAR(20) NOT NULL,
    factura VARCHAR(50),
    FOREIGN KEY (id_proveedor) REFERENCES Proveedores(id_proveedor) ON UPDATE CASCADE,
    FOREIGN KEY (id_empleado) REFERENCES Empleados(id_empleado) ON UPDATE CASCADE
);

CREATE TABLE DetalleCompra (
    id_detalle INT AUTO_INCREMENT PRIMARY KEY,
    id_compra INT NOT NULL,
    codigo_barras VARCHAR(20) NOT NULL,
    cantidad DECIMAL(10,3) NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    iva DECIMAL(10,2) NOT NULL,
    ieps DECIMAL(10,2) DEFAULT 0,
    importe DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_compra) REFERENCES Compras(id_compra) ON DELETE CASCADE,
    FOREIGN KEY (codigo_barras) REFERENCES Articulos(codigo_barras) ON UPDATE CASCADE
);

CREATE TABLE Inventario (
    id_movimiento INT AUTO_INCREMENT PRIMARY KEY,
    codigo_barras VARCHAR(20) NOT NULL,
    tipo_movimiento VARCHAR(10) NOT NULL,
    cantidad DECIMAL(10,3) NOT NULL,
    fecha_hora DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    id_referencia INT,
    tipo_referencia VARCHAR(10),
    motivo VARCHAR(100),
    id_empleado INT NOT NULL,
    FOREIGN KEY (codigo_barras) REFERENCES Articulos(codigo_barras) ON UPDATE CASCADE,
    FOREIGN KEY (id_empleado) REFERENCES Empleados(id_empleado) ON UPDATE CASCADE
);

CREATE TABLE Promociones (
    id_promocion INT AUTO_INCREMENT PRIMARY KEY,
    codigo_barras VARCHAR(20) NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    precio_promocion DECIMAL(10,2) NOT NULL,
    activa BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (codigo_barras) REFERENCES Articulos(codigo_barras) ON UPDATE CASCADE
);

CREATE TABLE PuntosClientes (
    id_movimiento INT AUTO_INCREMENT PRIMARY KEY,
    telefono_cliente CHAR(10) NOT NULL,
    id_venta INT,
    puntos INT NOT NULL,
    fecha_hora DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    tipo_movimiento VARCHAR(10) NOT NULL,
    FOREIGN KEY (telefono_cliente) REFERENCES Clientes(telefono) ON UPDATE CASCADE,
    FOREIGN KEY (id_venta) REFERENCES Ventas(id_venta) ON UPDATE CASCADE
);

CREATE TABLE Configuracion (
    id_config INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    valor VARCHAR(200) NOT NULL,
    descripcion VARCHAR(200)
);

show tables;
show databases;
select * from Empleados;
select * from Horarios;


INSERT INTO Categorias (nombre, descripcion) VALUES
('Bebidas', 'Bebidas en general'),
('Snacks', 'Botanas y frituras'),
('Lácteos', 'Productos derivados de la leche'),
('Panadería', 'Pan y productos horneados'),
('Abarrotes', 'Productos básicos del hogar'),
('Limpieza', 'Productos de limpieza'),
('Higiene', 'Cuidado personal'),
('Mascotas', 'Alimentos y accesorios'),
('Congelados', 'Alimentos congelados'),
('Farmacia', 'Medicamentos de venta libre');

INSERT INTO Proveedores (nombre, rfc, direccion, telefono, email) VALUES
('Distribuidora La Favorita', 'DFL010203ABC', 'Calle 1, Ciudad A', '5512345678', 'contacto@favorita.com'),
('Bebidas México', 'BMX040506DEF', 'Avenida 2, Ciudad B', '5523456789', 'ventas@bebmex.com'),
('Panaderia Express', 'PEX070809GHI', 'Calle 3, Ciudad C', '5534567890', 'pan@express.com'),
('Abarrotes El Centro', 'AEC101112JKL', 'Plaza 4, Ciudad D', '5545678901', 'contacto@abarrotes.com'),
('Lácteos del Norte', 'LDN131415MNO', 'Carrera 5, Ciudad E', '5556789012', 'ventas@lacteos.com'),
('Higiene Plus', 'HPL161718PQR', 'Calle 6, Ciudad F', '5567890123', 'info@higieneplus.com'),
('Super Limpio', 'SLI192021STU', 'Avenida 7, Ciudad G', '5578901234', 'ventas@superlimpio.com'),
('Mascotitas SA', 'MSA222324VWX', 'Calle 8, Ciudad H', '5589012345', 'contacto@mascotitas.com'),
('CongelaTodo', 'CTO252627YZA', 'Carretera 9, Ciudad I', '5590123456', 'ventas@congelatodo.com'),
('Farmacia Salud', 'FSA282930BCD', 'Boulevard 10, Ciudad J', '5501234567', 'farmacia@salud.com');

INSERT INTO Articulos (codigo_barras, nombre, id_categoria, id_proveedor, precio_venta, precio_compra, existencia, unidad_medida) VALUES
('000000000001', 'Coca-Cola 600ml', 1, 2, 15.00, 10.00, 100.000, 'pieza'),
('000000000002', 'Sabritas 45g', 2, 1, 12.00, 8.00, 200.000, 'pieza'),
('000000000003', 'Leche Lala 1L', 3, 5, 20.00, 15.00, 50.000, 'litro'),
('000000000004', 'Pan Blanco Bimbo', 4, 3, 28.00, 20.00, 60.000, 'pieza'),
('000000000005', 'Frijoles Bayos 1kg', 5, 4, 30.00, 22.00, 80.000, 'kg'),
('000000000006', 'Cloro 1L', 6, 7, 18.00, 12.00, 70.000, 'litro'),
('000000000007', 'Shampoo Sedal 350ml', 7, 6, 35.00, 25.00, 40.000, 'pieza'),
('000000000008', 'Croquetas DogChow 5kg', 8, 8, 250.00, 200.00, 30.000, 'kg'),
('000000000009', 'Pizza Congelada', 9, 9, 55.00, 40.00, 25.000, 'pieza'),
('000000000010', 'Paracetamol 500mg', 10, 10, 10.00, 5.00, 150.000, 'pieza');

INSERT INTO Empleados 
(nombre, apellido_paterno, apellido_materno, rfc, curp, direccion, telefono, email, fecha_nacimiento, fecha_contratacion, puesto, salario) VALUES
('Ana', 'García', 'López', 'GAL010101ABC', 'GAL010101MDFRPN01', 'Calle 10', '5611111111', 'ana@neto.com', '1990-01-01', '2022-01-15', 'Cajera', 8000.00),
('Luis', 'Pérez', 'Martínez', 'PMR020202DEF', 'PMR020202HDFLRS02', 'Calle 11', '5622222222', 'luis@neto.com', '1988-02-02', '2022-02-20', 'Supervisor', 12000.00),
('Clara', 'Torres', 'Ramírez', 'CTR030303GHI', 'CTR030303MDFLSR03', 'Calle 12', '5633333333', 'clara@neto.com', '1992-03-03', '2023-03-01', 'Vendedora', 8500.00),
('Miguel', 'Rodríguez', 'Díaz', 'MRD040404JKL', 'MRD040404HDFRDZ04', 'Calle 13', '5644444444', 'miguel@neto.com', '1995-04-04', '2023-04-10', 'Bodeguero', 9000.00),
('Sofía', 'Hernández', 'Cruz', 'SHC050505MNO', 'SHC050505MDFHRN05', 'Calle 14', '5655555555', 'sofia@neto.com', '1993-05-05', '2021-05-15', 'Gerente', 15000.00),
('Pedro', 'Gómez', 'Nava', 'PGN060606PQR', 'PGN060606HDFGMZ06', 'Calle 15', '5666666666', 'pedro@neto.com', '1985-06-06', '2021-06-20', 'Repartidor', 7500.00),
('Laura', 'Morales', 'Zapata', 'LMZ070707STU', 'LMZ070707MDFMLR07', 'Calle 16', '5677777777', 'laura@neto.com', '1991-07-07', '2020-07-25', 'Cajera', 8000.00),
('Carlos', 'Vega', 'Ruiz', 'CVR080808VWX', 'CVR080808MDFVGR08', 'Calle 17', '5688888888', 'carlos@neto.com', '1987-08-08', '2019-08-30', 'Jefe de piso', 11000.00),
('Mónica', 'Salinas', 'Reyes', 'MSR090909YZA', 'MSR090909MDFSLN09', 'Calle 18', '5699999999', 'monica@neto.com', '1994-09-09', '2022-09-05', 'Auxiliar', 7000.00),
('Javier', 'López', 'Ortiz', 'JLO101010BCD', 'JLO101010HDFLPR10', 'Calle 19', '5600000000', 'javier@neto.com', '1996-10-10', '2023-10-10', 'Seguridad', 8500.00);

INSERT INTO Horarios (id_empleado, dia_semana, hora_entrada, hora_salida) VALUES
(800414, 1, '09:00:00', '17:00:00'),
(800414, 2, '09:00:00', '17:00:00'),
(800415, 1, '08:00:00', '16:00:00'),
(800415, 2, '08:00:00', '16:00:00'),
(800416, 3, '10:00:00', '18:00:00'),
(800416, 4, '10:00:00', '18:00:00'),
(800417, 1, '07:00:00', '15:00:00'),
(800418, 5, '09:00:00', '17:00:00'),
(800419, 6, '12:00:00', '20:00:00'),
(800420, 7, '10:00:00', '18:00:00');


SELECT id_empleado, nombre FROM Empleados ORDER BY id_empleado;

INSERT INTO Clientes (telefono, nombre, apellido_paterno, apellido_materno, email, fecha_nacimiento) VALUES
('5610000001', 'Juan', 'Pérez', 'Gómez', 'juan@example.com', '1980-01-01'),
('5610000002', 'María', 'López', 'Díaz', 'maria@example.com', '1985-02-02'),
('5610000003', 'Pedro', 'Martínez', 'Hernández', 'pedro@example.com', '1990-03-03'),
('5610000004', 'Luisa', 'González', 'Ramírez', 'luisa@example.com', '1995-04-04'),
('5610000005', 'José', 'Rodríguez', 'Flores', 'jose@example.com', '1992-05-05'),
('5610000006', 'Ana', 'Sánchez', 'Luna', 'ana.s@example.com', '1989-06-06'),
('5610000007', 'Miguel', 'Cruz', 'Reyes', 'miguel@example.com', '1988-07-07'),
('5610000008', 'Laura', 'Torres', 'Salinas', 'laura@example.com', '1993-08-08'),
('5610000009', 'Jorge', 'Vega', 'Morales', 'jorge@example.com', '1991-09-09'),
('5610000010', 'Claudia', 'Nava', 'Zapata', 'claudia@example.com', '1987-10-10');

INSERT INTO Cajas (nombre, ubicacion) VALUES
('Caja 1', 'Entrada'),
('Caja 2', 'Centro'),
('Caja 3', 'Salida'),
('Caja 4', 'Zona A'),
('Caja 5', 'Zona B'),
('Caja 6', 'Zona C'),
('Caja 7', 'Farmacia'),
('Caja 8', 'Electrónica'),
('Caja 9', 'Juguetería'),
('Caja 10', 'Bodega');

INSERT INTO AperturasCaja (id_caja, id_empleado, monto_inicial) VALUES
(3443223, 800414, 1000.00),
(9292992, 800415, 1200.00),
(9292993, 800416,  800.00),
(9292994, 800417, 1500.00),
(9292995, 800418, 1300.00),
(9292996, 800419, 1000.00),
(9292997, 800420,  950.00),
(9292998, 800421, 1100.00),
(9292999, 800422,  900.00),
(9293000, 800423, 1000.00);

INSERT INTO Ventas (id_apertura, telefono_cliente, subtotal, iva, total, forma_pago, efectivo_recibido, cambio) VALUES
(11, '5610000001', 100.00, 16.00, 116.00, 'Efectivo', 120.00, 4.00),
(12, '5610000002', 80.00, 12.80, 92.80, 'Tarjeta', NULL, NULL),
(13, '5610000003', 150.00, 24.00, 174.00, 'Efectivo', 200.00, 26.00),
(14, '5610000004', 200.00, 32.00, 232.00, 'Transferencia', NULL, NULL),
(15, '5610000005', 50.00, 8.00, 58.00, 'Efectivo', 60.00, 2.00),
(16, '5610000006', 75.00, 12.00, 87.00, 'Efectivo', 100.00, 13.00),
(17, '5610000007', 120.00, 19.20, 139.20, 'Tarjeta', NULL, NULL),
(18, '5610000008', 90.00, 14.40, 104.40, 'Transferencia', NULL, NULL),
(19, '5610000009', 65.00, 10.40, 75.40, 'Efectivo', 80.00, 4.60),
(20, '5610000010', 110.00, 17.60, 127.60, 'Efectivo', 130.00, 2.40);


SELECT id_apertura, id_caja, id_empleado FROM AperturasCaja;
