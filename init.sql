-- ========================================
-- Script de inicialización de BD
-- Se ejecuta automáticamente en el primer arranque
-- ========================================

USE bluelabel_db;

-- Crear tabla info
CREATE TABLE IF NOT EXISTS info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    message VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insertar dato de prueba
INSERT INTO info (message) VALUES ('Hello from BlueLabel DevOps! 🚀');
