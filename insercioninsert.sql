-- Inserciones para la tabla empresa
INSERT INTO empresa (id_empresa, nombre, fecha_registro) VALUES
  (1, 'Interbank', DATE '2025-07-10'),
  (2, 'BanBif', DATE '2025-07-10'),
  (3, 'BancodelaNacion', DATE '2025-07-10'),
  (4, 'BCRP', DATE '2025-07-10'),
  (5, 'BancoPichincha', DATE '2025-07-10'),
  (6, 'BBVA', DATE '2025-07-10'),
  (7, 'BCP', DATE '2025-07-10'),
  (8, 'ScotiabankPE', DATE '2025-07-10');

-- Inserciones para la tabla usuario (cuentas sociales asociadas a empresa)
INSERT INTO usuario (id_usuario, id_empresa, cuenta, nombre, fecha_registro) VALUES
  (1, 1, 'Interbank', 'Interbank', DATE '2025-07-10'),
  (2, 2, 'BanBif', 'Banco Interamericano de Finanzas (BanBif)', DATE '2025-07-10'),
  (3, 3, 'BancodelaNacion', 'Banco de la Nación', DATE '2025-07-10'),
  (4, 4, 'bcrpoficial', 'Banco Central de Reserva del Perú (BCRP)', DATE '2025-07-10'),
  (5, 5, 'BancoPichincha', 'Banco Pichincha', DATE '2025-07-10'),
  (6, 6, 'bbva_peru', 'BBVA Perú', DATE '2025-07-10'),
  (7, 7, 'BCPComunica', 'Banco de Crédito del Perú (BCP)', DATE '2025-07-10'),
  (8, 8, 'ScotiabankPE', 'Scotiabank Perú', DATE '2025-07-10');

-- Inserciones para la tabla usuario_acceso (usuarios JWT para autenticación)
-- Contraseñas hasheadas con bcrypt (password: "password123")
INSERT INTO usuario_acceso (id_usuario_acceso, username, password_hash, id_empresa, rol, activo) VALUES
  (1, 'admin_interbank', '$2b$12$1jXfeJ71UhUbNT8ZijnxoOkSB.8erlTb4z0UbbK0R7bDT/bH.oKTW', 1, 'admin', TRUE),
  (2, 'admin_banbif', '$2b$12$1jXfeJ71UhUbNT8ZijnxoOkSB.8erlTb4z0UbbK0R7bDT/bH.oKTW', 2, 'admin', TRUE),
  (3, 'admin_nacion', '$2b$12$1jXfeJ71UhUbNT8ZijnxoOkSB.8erlTb4z0UbbK0R7bDT/bH.oKTW', 3, 'admin', TRUE),
  (4, 'admin_bcrp', '$2b$12$1jXfeJ71UhUbNT8ZijnxoOkSB.8erlTb4z0UbbK0R7bDT/bH.oKTW', 4, 'admin', TRUE),
  (5, 'admin_pichincha', '$2b$12$1jXfeJ71UhUbNT8ZijnxoOkSB.8erlTb4z0UbbK0R7bDT/bH.oKTW', 5, 'admin', TRUE),
  (6, 'admin_bbva', '$2b$12$1jXfeJ71UhUbNT8ZijnxoOkSB.8erlTb4z0UbbK0R7bDT/bH.oKTW', 6, 'admin', TRUE),
  (7, 'admin_bcp', '$2b$12$1jXfeJ71UhUbNT8ZijnxoOkSB.8erlTb4z0UbbK0R7bDT/bH.oKTW', 7, 'admin', TRUE),
  (8, 'admin_scotiabank', '$2b$12$1jXfeJ71UhUbNT8ZijnxoOkSB.8erlTb4z0UbbK0R7bDT/bH.oKTW', 8, 'admin', TRUE),
  (9, 'user_interbank', '$2b$12$1jXfeJ71UhUbNT8ZijnxoOkSB.8erlTb4z0UbbK0R7bDT/bH.oKTW', 1, 'user', TRUE),
  (10, 'user_bcp', '$2b$12$1jXfeJ71UhUbNT8ZijnxoOkSB.8erlTb4z0UbbK0R7bDT/bH.oKTW', 7, 'user', TRUE),
  (11, 'viewer_bbva', '$2b$12$1jXfeJ71UhUbNT8ZijnxoOkSB.8erlTb4z0UbbK0R7bDT/bH.oKTW', 6, 'viewer', TRUE),
  (12, 'inactive_user', '$2b$12$1jXfeJ71UhUbNT8ZijnxoOkSB.8erlTb4z0UbbK0R7bDT/bH.oKTW', 1, 'user', FALSE);

/*
=============================================================================
INFORMACIÓN DE PRUEBAS JWT
=============================================================================

CREDENCIALES DE PRUEBA (todas usan password: "password123"):

ADMINISTRADORES (rol: admin):
- admin_interbank    → Empresa: Interbank      → Acceso: Interbank
- admin_banbif       → Empresa: BanBif         → Acceso: BanBif  
- admin_nacion       → Empresa: BancodelaNacion → Acceso: BancodelaNacion
- admin_bcrp         → Empresa: BCRP           → Acceso: bcrpoficial
- admin_pichincha    → Empresa: BancoPichincha → Acceso: BancoPichincha
- admin_bbva         → Empresa: BBVA           → Acceso: bbva_peru
- admin_bcp          → Empresa: BCP            → Acceso: BCPComunica
- admin_scotiabank   → Empresa: ScotiabankPE   → Acceso: ScotiabankPE

USUARIOS REGULARES (rol: user):
- user_interbank     → Empresa: Interbank      → Acceso limitado
- user_bcp           → Empresa: BCP            → Acceso limitado

VISUALIZADORES (rol: viewer):
- viewer_bbva        → Empresa: BBVA           → Solo lectura

USUARIOS INACTIVOS (para testing):
- inactive_user      → Cuenta desactivada      → Sin acceso

=============================================================================
EJEMPLOS DE TESTING JWT:
=============================================================================

1. LOGIN EXITOSO:
   curl -X POST "http://localhost:8000/auth/login" \
   -H "Content-Type: application/json" \
   -d '{"username": "admin_interbank", "password": "password123"}'

2. ACCESO PERMITIDO (mismo empresa):
   curl -H "Authorization: Bearer TOKEN" \
   "http://localhost:8000/regression/predict/Interbank?fecha=2025-07-11"

3. ACCESO DENEGADO (diferente empresa):
   curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbl9pbnRlcmJhbmsiLCJlbXByZXNhX2lkIjoxLCJyb2wiOiJhZG1pbiIsImV4cCI6MTc1MjIzNTIyM30.Swt3_sMhntX-QX8TfUL6zCrOiRvSUNXYi1P6xpu2rho" \
   "http://localhost:8000/regression/predict/BCPComunica?fecha=2025-07-11"

4. SIN AUTENTICACIÓN (error 401):
   curl "http://localhost:8000/regression/predict/Interbank?fecha=2025-07-11"

5. CUENTA INACTIVA:
   curl -X POST "http://localhost:8000/auth/login" \
   -H "Content-Type: application/json" \
   -d '{"username": "inactive_user", "password": "password123"}'

=============================================================================
*/
