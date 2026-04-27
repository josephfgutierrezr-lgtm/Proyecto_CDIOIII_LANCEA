# Protocolo de Pruebas Industrial — Proyecto LANCEA
**Versión:** 2.1 | **Fecha de actualización:** 2026-04-27
**Equipo:** Joseph Fernando Gutiérrez · Emerson Santiago Córdoba · Johan Rodrigo Piedrahita

> ⚠️ Este protocolo ha sido diligenciado y ejecutado. Los resultados definitivos se encuentran registrados en `Bitacora_Trazabilidad.csv`.

---

## TEST-HW-01-A — Validación Dimensional PCB (KiCad)
**Prioridad:** P1 Alto | **Requisito:** REQ-HW-01 | **Estado:** ✅ PASS

| Campo | Detalle |
|---|---|
| Objetivo | Validar que el ancho de la PCB permita encaje aerodinámico dentro del Sled (Ø 24mm) |
| Setup | Software KiCad 7.0, Diseño 3D del chasis Sled |
| Pasos | 1. Trazar bordes de corte (Edge.Cuts) · 2. Medir ancho máximo en KiCad · 3. Comparar con Ø interno del Sled (24mm) |
| Input | Ancho máx objetivo: ≤ 20mm |
| Resultado Esperado | Placa virtual ≤ 20mm de ancho |
| Resultado Obtenido | **19.8mm** ✅ |
| Responsable | Joseph Gutiérrez |

---

## TEST-FW-01-A — Validación Ángulo IMU (Estático)
**Prioridad:** P0 Crítico | **Requisito:** REQ-FW-01 | **Estado:** ✅ PASS

| Campo | Detalle |
|---|---|
| Objetivo | Validar lectura de ángulo de inclinación (Pitch/Roll) del BNO055 en condición estática |
| Setup | ESP32-C3, BNO055, Protoboard, Monitor Serial 115200 baud, Escuadra física 45° |
| Pasos | 1. Flashear firmware I2C · 2. Posicionar sensor a 0° plano · 3. Inclinar a 45° sobre escuadra · 4. Registrar lectura |
| Input | Baudrate: 115200 · Ángulo físico: 45° exactos |
| Resultado Esperado | Lectura en Monitor Serial: 45° ± 2° |
| Resultado Obtenido | **44.5° – 45.1°** ✅ |
| Responsable | Joseph Gutiérrez |

---

## TEST-MC-01-A — Validación de Autonomía
**Prioridad:** P0 Crítico | **Requisito:** REQ-HW-02 | **Estado:** ✅ PASS

| Campo | Detalle |
|---|---|
| Objetivo | Validar tiempo de operación continua con batería Li-Ion 14500 |
| Setup | Batería 14500 (1000mAh) al 100%, ESP32 en modo activo, Cronómetro |
| Pasos | 1. Conectar batería al circuito · 2. Registrar hora de inicio · 3. Monitorear hasta corte BMS (V_min = 3.0V) |
| Input | Consumo estimado: ~120mA · V_corte: 3.0V |
| Resultado Esperado | ≥ 6 horas de operación continua |
| Resultado Obtenido | **7 horas 15 minutos** ✅ |
| Responsable | Joseph Gutiérrez |

---

## TEST-HW-01-B — Inspección Dimensional Jabalina
**Prioridad:** P1 Alto | **Requisito:** REQ-HW-01 | **Estado:** ✅ PASS

| Campo | Detalle |
|---|---|
| Objetivo | Confirmar que el diámetro interno de la jabalina acepta el chasis Sled |
| Setup | Jabalina de entrenamiento profesional, Calibrador Pie de Rey |
| Pasos | 1. Revisar punto de inserción · 2. Medir diámetro interno con Pie de Rey · 3. Comparar con ancho del Sled |
| Input | Diámetro mínimo requerido: > 24mm |
| Resultado Esperado | Diámetro interno > 24mm |
| Resultado Obtenido | **25.2mm** — holgura suficiente ✅ |
| Responsable | Joseph, Rodrigo, Emerson |

---

## TEST-FW-02 — Validación Tasa de Muestreo 100Hz
**Prioridad:** P1 Alto | **Requisito:** REQ-FW-01 | **Estado:** ✅ PASS (Corregido)

| Campo | Detalle |
|---|---|
| Objetivo | Confirmar que el firmware logra exactamente 100Hz en la grabación de datos |
| Setup | Firmware de producción, función `micros()` del ESP32 |
| Pasos | 1. Iniciar grabación · 2. Almacenar 1000 muestras · 3. Calcular Δt entre muestras en CSV · 4. Calcular desviación estándar |
| Input | Target: 10ms por muestra (Δt = 10000 µs) |
| Resultado Esperado | σ(Δt) < 1ms |
| Resultado Obtenido | **σ(Δt) < 1ms — Jitter eliminado exitosamente (Adquisición independiente mediante ISR implementada)** ✅ |
| Responsable | Joseph Gutiérrez |

---

## TEST-MC-01-B — Validación Integridad Datos SD/SPI
**Prioridad:** P0 Crítico | **Requisito:** REQ-MC-01 | **Estado:** ✅ PASS (Corregido)

| Campo | Detalle |
|---|---|
| Objetivo | Validar que la escritura en MicroSD no interfiera ni corrompa la lectura del IMU BNO055 |
| Setup | Sled ensamblado completo, Batería 14500 al 100% |
| Pasos | 1. Activar sistema · 2. Realizar movimientos en 3 ejes durante 30s · 3. Extraer SD · 4. Graficar datos en Python |
| Input | Duración de estrés: 30 segundos |
| Resultado Esperado | Datos sin huecos y sin ruido eléctrico por picos de consumo SD |
| Resultado Obtenido | **Escritura continua sin huecos ni interferencias de voltaje (Buffer RAM y capacitores instalados)** ✅ |
| Responsable | C. Rojas |

---

## TEST-HW-01-C — Ajuste Mecánico Final Chasis
**Prioridad:** P2 Medio | **Requisito:** REQ-HW-01 | **Estado:** ✅ PASS (Corregido)

| Campo | Detalle |
|---|---|
| Objetivo | Validar ajuste mecánico sin vibración del Sled dentro de la jabalina |
| Setup | Sled impreso en PETG, Jabalina profesional, Pie de Rey |
| Pasos | 1. Introducir Sled en jabalina · 2. Agitar longitudinalmente · 3. Escuchar/verificar holgura |
| Input | Diámetro tubo < 25mm |
| Resultado Esperado | Sled entra suavemente y **no suena** al agitar |
| Resultado Obtenido | **Ajuste firme, sin holgura ni sonido al agitar (O-Rings de compresión instalados correctamente)** ✅ |
| Responsable | Rodrigo, Emerson, Joseph |

---

## TEST-FW-01-B — Prueba de Campo (Trigger de Lanzamiento)
**Prioridad:** P0 Crítico | **Requisito:** REQ-FW-02 | **Estado:** ✅ PASS (Corregido)

| Campo | Detalle |
|---|---|
| Objetivo | Validar detección automática del lanzamiento por aceleración en condición real de campo |
| Setup | Sistema completo dentro de jabalina, Campo de atletismo |
| Pasos | 1. Armar sistema (LED lento = listo) · 2. Ejecutar lanzamiento real · 3. Recuperar Sled · 4. Verificar LED + archivo CSV |
| Input | Umbral: JERK_THRESHOLD ajustado |
| Resultado Esperado | LED destella 3 veces + archivo CSV con lanzamiento registrado |
| Resultado Obtenido | **Lanzamiento detectado y registrado correctamente en CSV tras calibración de umbrales (JERK_THRESHOLD optimizado)** ✅ |
| Responsable | Rodrigo |
