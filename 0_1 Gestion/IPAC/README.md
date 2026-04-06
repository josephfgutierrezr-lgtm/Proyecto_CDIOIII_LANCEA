# Retrospectiva IPAC — Lecciones Aprendidas
**Proyecto:** LANCEA | **Ciclo:** IPAC-03 → IPAC-04
**Fecha:** 2026-04-06 | **Facilitador:** Equipo Lancea

---

## 🔴 ¿Qué falló?

### Fallo 1 — Jitter en muestreo 100Hz (TEST-FW-02 ❌)
**Síntoma:** El delta de tiempo entre muestras varía más de 1ms, comprometiendo la calidad del análisis biomecánico.
**Causa raíz:** El ciclo `loop()` del firmware mezcla adquisición de datos con escritura en SD Card. Las operaciones SD bloquean el bus SPI, causando que el IMU sea leído con retardos variables.
**Impacto:** Los datos cinemáticos (velocidad, ángulo) tienen incertidumbre temporal que invalida cálculos de jerk precisos.

### Fallo 2 — Ruido SD corrompe datos IMU (TEST-MC-01-B ❌)
**Síntoma:** Al escribir en la MicroSD, aparecen huecos y picos de voltaje en los datos del BNO055.
**Causa raíz:** La escritura muestra a muestra genera picos de consumo corriente de hasta ~100mA en la línea VCC, causando caídas de tensión que afectan la comunicación I2C con el BNO055.
**Impacto:** Pérdida de muestras y posibles lecturas corruptas durante los momentos críticos del lanzamiento.

### Fallo 3 — Holgura mecánica del Sled (TEST-HW-01-C ❌)
**Síntoma:** El Sled suena al agitar la jabalina longitudinalmente.
**Causa raíz:** Las tolerancias de impresión 3D en PETG no consideraron las dilataciones térmicas ni las vibraciones de alta frecuencia del tubo de fibra de carbono de la jabalina.
**Impacto:** Movimiento relativo del Sled introduce aceleraciones parásitas que el BNO055 registra como datos falsos.

### Fallo 4 — Trigger de campo no detectó lanzamiento (TEST-FW-01-B ❌)
**Síntoma:** El sistema no generó el archivo CSV durante el lanzamiento real.
**Causa raíz:** El parámetro `JERK_THRESHOLD` fue calibrado en laboratorio con una sacudida de escritorio (~30 m/s³) y puede ser demasiado elevado para las condiciones reales del lanzamiento en campo.
**Impacto:** Cero datos capturados en la prueba de campo — el sistema no es funcional en condición real aún.

---

## ✅ Acciones Correctivas Implementadas / Planificadas

| # | Acción | Tipo | Estado | Responsable |
|---|---|---|---|---|
| AC-01 | Implementar ISR con Timer de Hardware para adquisición de datos a 100Hz estrictos | Firmware | 🚧 En progreso | Joseph Gutiérrez |
| AC-02 | Buffer circular en RAM para acumular muestras y escribir SD en bloques | Firmware | 🚧 En progreso | Joseph Gutiérrez |
| AC-03 | Soldar capacitores de desacoplo 100µF + 0.1µF en línea VCC del módulo SD | Hardware | 📋 Planificado | C. Rojas |
| AC-04 | Instalar O-Rings de compresión en ranuras radiales del chasis PETG | Mecánica | ✅ Implementado | Rodrigo / Emerson |
| AC-05 | Activar DEBUG_MODE 1, medir Jerk real en campo, ajustar JERK_THRESHOLD | Firmware | 📋 Planificado | Rodrigo |
| AC-06 | Condensador 10µF entre RST y GND para evitar reset al desconectar USB | Hardware | 📋 Planificado | Joseph Gutiérrez |

---

## 💡 Lo que funcionó bien (Mantener)

1. **Arquitectura WiFi Store-and-Forward (FSM 3 estados):** El servidor web nunca se bloquea aunque el firmware esté midiendo. Diseño robusto.
2. **Dashboard Python v3.0:** La interfaz CustomTkinter con 5 módulos es intuitiva y el reporte automático en PDF ahorra tiempo en campo.
3. **Validación dimensional temprana (Test-driven HW):** Medir la jabalina y la PCB antes de fabricar evitó retrabajos costosos.
4. **Autonomía de batería:** 7h15m superó el objetivo de 6h con margen suficiente para sesiones largas.

---

## 📌 Compromisos para IPAC-04

- [ ] ISR Timer implementado y TEST-FW-02 en estado PASS antes del **2026-04-20**
- [ ] Buffer RAM implementado y TEST-MC-01-B en estado PASS antes del **2026-04-20**
- [ ] Capacitores soldados y TEST-MC-01-B re-ejecutado antes del **2026-04-18**
- [ ] JERK_THRESHOLD re-calibrado y TEST-FW-01-B re-ejecutado en campo antes del **2026-04-25**
