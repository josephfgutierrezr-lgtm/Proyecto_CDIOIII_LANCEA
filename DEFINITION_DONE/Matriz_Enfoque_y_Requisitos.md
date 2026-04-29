# Matriz de Enfoque y Requisitos — Proyecto LANCEA
**Universidad del Quindío | Ingeniería Electrónica | 2025–2026**
**Equipo:** Joseph Fernando Gutiérrez · Emerson Santiago Córdoba · Johan Rodrigo Piedrahita

---

## 1. Historia de Usuario y Valor de Negocio

| ID | Historia de Usuario | Valor (1–5) | Riesgo Técnico (1–5) | Prioridad |
|----|---|:---:|:---:|:---:|
| HU-01 | Como entrenador, quiero ver la velocidad y ángulo de lanzamiento en tiempo real para corregir la técnica del atleta inmediatamente. | 5 | 4 | **P0** |
| HU-02 | Como atleta, quiero que el sistema sea invisible dentro de la jabalina para no alterar su vuelo. | 5 | 5 | **P0** |
| HU-03 | Como técnico, quiero descargar los datos en CSV desde el teléfono sin cables para agilizar el análisis post-sesión. | 4 | 3 | **P1** |
| HU-04 | Como investigador, quiero que el sistema registre 100 muestras/segundo para análisis biomecánico de precisión. | 5 | 5 | **P0** |
| HU-05 | Como usuario en campo, quiero que la batería dure al menos 6 horas para cubrir una sesión completa de entrenamiento. | 4 | 2 | **P1** |

---

## 2. Matriz de Requisitos Técnicos

| ID Req. | Requisito | Especificación Medible | Validado por |
|---------|---|---|---|
| REQ-HW-01 | Dimensión del Sled | Ancho ≤ 20 mm para encaje en tubo de 25.2 mm | TEST-HW-01 ✅ |
| REQ-HW-02 | Autonomía de batería | ≥ 6 horas en modo activo continuo | TEST-MC-01 ✅ |
| REQ-FW-01 | Tasa de muestreo IMU | 100 Hz exactos (Δt = 10ms ± 1ms) |  TEST-HW-01 ✅  |
| REQ-FW-02 | Detección de lanzamiento | Trigger con aceleración > 15 m/s² (JERK > 50 m/s³) |  TEST-HW-01 ✅  |
| REQ-MC-01 | Integridad de datos SD | 0 huecos en datos durante 30s de estrés mecánico |  TEST-HW-01 ✅  |
| REQ-SW-01 | Transmisión WiFi | Servidor web accesible en 192.168.4.1 con SSID LANCEA_AP | Validado v7.0 |
| REQ-SW-02 | Dashboard Python | Visualización en tiempo real + exportación de reportes automáticos | Validado v3.0 |

---

## 3. Hardware Backlog y Presupuesto (BOM)

### Electrónica Principal

| Ítem | Componente | Cant. | Especificación | Est. Costo (COP) |
|------|---|:---:|---|:---:|
| 1 | Microcontrolador | 1 | XIAO ESP32-C3 (WiFi 2.4GHz) | $25.000 |
| 2 | IMU (Sensor) | 1 | Adafruit BNO055 (9-DOF, fusión inercial) | $120.000 |
| 3 | Pantalla | 1 | OLED 0.91" I2C (128×32) | $15.000 |
| 4 | Módulo MicroSD | 1 | Interfaz SPI | $8.000 |
| 5 | Tarjeta Memoria | 1 | MicroSD 16GB Clase 10 | $20.000 |

### Sistema de Potencia

| Ítem | Componente | Cant. | Especificación | Est. Costo (COP) |
|------|---|:---:|---|:---:|
| 6 | Batería | 1 | Li-Ion 14500 (3.7V ~800mAh) | $18.000 |
| 7 | Cargador | 1 | TP4056 con USB-C y protección | $3.500 |
| 8 | Interruptor | 1 | Slide Switch SPDT Mini | $1.000 |
| 9 | Portapilas | 1 | Holder 14500 PCB Mount | $2.500 |

### Mecánica e Insumos

| Ítem | Componente | Cant. | Especificación | Est. Costo (COP) |
|------|---|:---:|---|:---:|
| 10 | Pulsador | 1 | Tact Switch 6×6mm | $500 |
| 11 | LED RGB | 1 | 5mm Cátodo Común | $1.000 |
| 12 | Resistencias | 3 | 220Ω, 10kΩ (1/4W) | $200 |
| 13 | PCB | 1 | Baquelita Universal Doble Cara | $5.000 |
| 14 | Filamento 3D | ~20g | PETG o PLA+ (Sled) | $5.000 |
| 15 | Varios | 1 | O-Rings, Cable 30AWG, Estaño | $10.000 |

### 💰 Resumen Presupuesto

| Categoría | Subtotal |
|---|:---:|
| Electrónica y Sensores | $188.000 |
| Potencia y Energía | $25.000 |
| Mecánica e Insumos | $21.700 |
| **TOTAL POR UNIDAD** | **$234.700 COP** |

---

## 4. Planificación MAHD — Ciclos IPAC

| IPAC | Objetivo | Fecha Inicio | Fecha Fin | Estado |
|------|---|---|---|---|
| IPAC-01 | Integración HW básica (ESP32 + BNO055) + firmware lectura serial | Sem. 1 | Sem. 3 | ✅ Done |
| IPAC-02 | Diseño PCB en KiCad + Sled 3D + pruebas dimensionales | Sem. 4 | Sem. 6 | ✅ Done |
| IPAC-03 | Firmware WiFi v7.0 + Dashboard Python v3.0 + pruebas de campo | Sem. 7 | Sem. 9 |  TEST-HW-01 ✅  |
| IPAC-04 | Corrección bugs (100Hz ISR }) + validación final | Sem. 10 | Sem. 12 |  TEST-HW-01 ✅  |
