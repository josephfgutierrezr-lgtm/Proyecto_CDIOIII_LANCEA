# Resultados de Diseño — Planos As-Built y Auditoría de Costos
**Proyecto:** LANCEA | **Versión:** 2.0 | **Fecha:** 2026-04-06

---

## 1. Esquemático Electrónico (As-Built)

### Mapa de Conexiones Confirmado

| Componente | Pin | ESP32-C3 (XIAO) | Función | Protocolo |
|---|---|---|---|---|
| **BNO055** | VCC | 3.3V | Alimentación sensor | — |
| **BNO055** | GND | GND | Tierra común | — |
| **BNO055** | SDA | D4 (GPIO 6) | Datos I²C | I²C 400kHz |
| **BNO055** | SCL | D5 (GPIO 7) | Reloj I²C | I²C 400kHz |
| **MicroSD** | CS | GPIO 20 | Chip Select | SPI |
| **MicroSD** | MOSI | GPIO 10 | Datos → SD | SPI |
| **MicroSD** | MISO | GPIO 9 | Datos ← SD | SPI |
| **MicroSD** | SCK | GPIO 8 | Reloj SPI | SPI |
| **LED RGB** | R | GPIO 2 | Estado IMPULSO | PWM |
| **LED RGB** | G | GPIO 3 | Estado IDLE | PWM |
| **LED RGB** | B | GPIO 4 | Estado PAUSA | PWM |
| **Batería** | + | BAT+ (TP4056 OUT) | Alimentación principal | LiPo 3.7V |

> 📎 Archivo KiCad: `Primer_esquematico_v1.kicad_pcb` — Repositorio: `/5_Resultados_Diseno/`

---

## 2. Dimensiones Mecánicas (As-Built)

| Parámetro | Diseño | Medido (As-Built) | Estado |
|---|:---:|:---:|:---:|
| Ancho máx. PCB | ≤ 20mm | **19.8mm** | ✅ Conforme |
| Longitud del Sled | ≤ 120mm | ~115mm | ✅ Conforme |
| Diámetro interno jabalina | ≥ 24mm | **25.2mm** | ✅ Conforme |
| Diámetro externo Sled (con O-Rings) | ≤ 25mm | ~24.8mm | 🚧 Validando |
| Material del chasis | PETG | PETG | ✅ Conforme |
| Peso total del sistema | ≤ 50g | ~42g (est.) | ✅ Conforme |

---

## 3. Auditoría de Costos Real (Actualizada a Feb 2026)

### Componentes Adquiridos

| Ítem | Componente | Precio Estimado | Precio Real (COP) | Δ Costo | Estado |
|------|---|:---:|:---:|:---:|:---:|
| 1 | XIAO ESP32-C3 | $25.000 | $27.500 | +$2.500 | ✅ Comprado |
| 2 | BNO055 IMU | $120.000 | $115.000 | -$5.000 | ✅ Comprado |
| 3 | OLED 0.91" I2C | $15.000 | $14.000 | -$1.000 | ✅ Comprado |
| 4 | Módulo MicroSD | $8.000 | $8.500 | +$500 | ✅ Comprado |
| 5 | MicroSD 16GB | $20.000 | $18.000 | -$2.000 | ✅ Comprado |
| 6 | Batería 14500 | $18.000 | $20.000 | +$2.000 | ✅ Comprado |
| 7 | TP4056 USB-C | $3.500 | $3.500 | $0 | ✅ Comprado |
| 8 | Slide Switch | $1.000 | $800 | -$200 | ✅ Comprado |
| 9 | Holder 14500 | $2.500 | $2.500 | $0 | ✅ Comprado |
| 10 | Pulsador 6x6mm | $500 | $500 | $0 | ✅ Comprado |
| 11 | LED RGB 5mm | $1.000 | $1.000 | $0 | ✅ Comprado |
| 12 | Resistencias | $200 | $200 | $0 | ✅ Comprado |
| 13 | PCB Baquelita | $5.000 | $6.000 | +$1.000 | ✅ Comprado |
| 14 | Filamento PETG 20g | $5.000 | $5.000 | $0 | ✅ Comprado |
| 15 | O-Rings + Insumos | $10.000 | $12.000 | +$2.000 | ✅ Comprado |

### Resumen Real vs Estimado

| Categoría | Estimado | Real | Δ |
|---|:---:|:---:|:---:|
| Electrónica y Sensores | $188.000 | $184.500 | -$3.500 |
| Potencia y Energía | $25.000 | $26.800 | +$1.800 |
| Mecánica e Insumos | $21.700 | $24.000 | +$2.300 |
| **TOTAL** | **$234.700** | **$235.300** | **+$600** |

> ✅ El proyecto se ejecutó dentro del presupuesto estimado con una variación de apenas **+0.26%**.

---

## 4. Referencias de Archivos

| Archivo | Descripción | Ubicación |
|---|---|---|
| `Primer_esquematico_v1.kicad_pcb` | Esquemático PCB en KiCad | GitHub `/5_Resultados_Diseno/` |
| `Manual_LANCEA_v2.0.pdf` | Manual técnico completo | GitHub `/5_Resultados_Diseno/` |
| `Dashboard_MAHD.xlsx` | Dashboard de seguimiento MAHD | GitHub (raíz) |
| `Protocolos_de_prueba.xlsx` | Protocolos V&V formales | GitHub `/4_Calidad_y_Pruebas/` |
