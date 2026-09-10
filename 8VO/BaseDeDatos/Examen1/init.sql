-- CRM básico: 
USE empresa_db;

CREATE TABLE IF NOT EXISTS empleados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    departamento VARCHAR(50)
);

INSERT INTO empleados (nombre, departamento) VALUES
('Juan Carlos Bodóque', 'Ventas'),
('Tulio Triviño', 'Marketing');
