## CHECKLIST DE DEFINICIÓN DE HECHO (DoD) - LANCEA

Antes de cerrar esta tarea y moverla a "Done", certifico como ingeniero a cargo que he validado lo siguiente en el prototipo base:

### ⚡ 1. HARDWARE
- [x] **Esquemático/PCB:** Actualizado en la carpeta `02_Hardware` sin errores de reglas de diseño (0 Errores DRC).
- [x] **Continuidad:** La placa pasó la prueba de cortos (0 cortos en pistas de potencia y buses I2C/SPI).
- [x] **Cero Parches:** No hay cables "voladores"; las conexiones del BNO055 y la MicroSD están ruteadas o soldadas firmemente.
- [x] **Métricas:** El módulo TP4056 entrega voltaje de carga estable y el ESP32 recibe sus 3.3V lógicos dentro de la tolerancia exigida.

### 💻 2. FIRMWARE/SOFTWARE
- [x] **Compilación limpia:** El código de prueba (Hola Mundo) compila con 0 Errores y 0 Warnings en PlatformIO/Arduino.
- [x] **Código No-Bloqueante:** No se usa la función `delay()` que detenga la adquisición de datos de la IMU.
- [x] **Repositorio:** El código está subido a la rama principal de GitHub (Push realizado).
- [x] **Trazabilidad:** El Commit incluye la palabra clave para cerrar esta tarea (Ej: `Closes #ID`).

### ⚙️ 3. MECÁNICA / DISEÑO 3D
- [x] **Archivos Fuente:** El diseño base del chasis cilíndrico ("Sled") está en la subcarpeta `Mechanical/`.
- [x] **Archivos de Fabricación:** El `.STL` final está subido y listo para imprimir en PETG/PLA+.
- [x] **Tolerancia:** Se validó matemáticamente que la PCB tipo "Strip" (20mm de ancho) cabe perfectamente en el diámetro interno de 24mm diseñado para la jabalina.

### 📋 4. GESTIÓN Y PRUEBAS
- [x] **BOM Actualizado:** Todos los componentes adquiridos (ESP32, BNO055, TP4056, Batería 14500) están costeados en la Lista de Materiales.
- [x] **Protocolo de Pruebas:** Se diligenció el archivo Excel Oficial de Pruebas (Test Report) para los subsistemas actuales.
- [x] **Aprobación:** La columna de "Estado Final" en el Excel de pruebas dice "✅ PASS" con datos reales (sin subjetividades).
