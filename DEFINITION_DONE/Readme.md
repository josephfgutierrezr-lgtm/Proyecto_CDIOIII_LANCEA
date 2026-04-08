# Definition of Done (DoD) — Proyecto LANCEA
**Versión:** 2.0 | **Aprobado por:** Equipo LANCEA | **Fecha:** 2026-04-06

---

## Criterios de Aceptación Globales
Los siguientes criterios definen las condiciones mínimas que deben cumplirse para considerar una tarea o iteración como finalizada dentro del proyecto. Estos garantizan calidad, trazabilidad y validación tanto en software como en hardware.
Para que cualquier tarea o iteración (IPAC) se considere terminada, debe cumplir obligatoriamente con TODOS los siguientes criterios:

| # | Criterio | Verificación |
|---|---|---|
| 1 | **Código compila:** El firmware en C++ compila sin errores ni warnings en Arduino IDE / PlatformIO. | CI / Compilación local |
| 2 | **Prueba física ejecutada:** El hardware (ESP32-C3 + BNO055) fue sometido al protocolo de prueba correspondiente. | Bitácora firmada |
| 3 | **Trazabilidad GitHub:** La rama fue fusionada a `main` con al menos 1 commit semántico descriptivo. | Pull Request cerrado |
| 4 | **Revisión documentada:** Existe aprobación técnica registrada para revisión con el profesor Luis Miguel Capacho. | Acta o comentario en issue |
| 5 | **Dashboard actualizado:** El estado de la tarea en el tablero Kanban refleja "Done" con fecha de cierre. | Tablero GitHub Projects |

---

## Criterios Específicos por Componente

### Firmware
En esta sección se validan los criterios relacionados con el comportamiento del software embebido, asegurando estabilidad temporal en la adquisición de datos y correcta detección de eventos clave durante el lanzamiento.

| Test ID | Parámetro | Tolerancia Aceptable | Estado |
|---------|---|---|:---:|
| TEST-FW-02 | Delta de tiempo entre muestras en CSV | σ < 1 ms (100 Hz estables) | ✅ Pass |
| TEST-FW-01 Campo | Detección de lanzamiento por jerk | Trigger con Jerk > 50 m/s³ | ✅ Pass |

### Hardware / Mecánica
Estos criterios verifican que las dimensiones físicas y el ensamblaje del sistema sean adecuados para su integración en la jabalina, garantizando ajuste correcto y funcionamiento sin fallas mecánicas.

| Test ID | Parámetro | Tolerancia Aceptable | Estado |
|---------|---|---|:---:|
| TEST-HW-01 PCB | Ancho del sled | ≤ 20 mm | ✅ Pass |
| TEST-HW-01 Dim. | Diámetro interno jabalina | ≥ 24 mm | ✅ Pass (25.2mm) |
| TEST-HW-01 Chasis | Ajuste mecánico sin holgura | Sin sonido al agitar | ❌ WIP |

### Sistema Integrado / Datos
En esta sección se evalúa el desempeño del sistema completo en condiciones reales de uso, incluyendo autonomía energética y confiabilidad en la captura y almacenamiento de datos.

| Test ID | Parámetro | Tolerancia Aceptable | Estado |
|---------|---|---|:---:|
| TEST-MC-01 Potencia | Autonomía en campo | ≥ 6 horas continuas | ✅ Pass (7h15m) |
| TEST-MC-01 SD | Integridad de datos durante grabación | 0 huecos, 0 picos de ruido | ❌ WIP |

---

## Lo que NO es "Done"
A continuación se listan situaciones que, aunque aparenten estar completas, no cumplen con los criterios mínimos definidos por el equipo para considerar una tarea como finalizada:

- ❌ "Funciona en mi máquina" sin prueba en hardware real
- ❌ Código en rama feature sin merge a main
- ❌ Prueba ejecutada pero no registrada en Bitácora_Trazabilidad
- ❌ Estado "Done" en el tablero sin evidencia fotográfica o log CSV
