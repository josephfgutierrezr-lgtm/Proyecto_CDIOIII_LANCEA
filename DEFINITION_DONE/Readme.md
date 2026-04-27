# 🚀 Definition of Done (DoD) — Proyecto LANCEA
**Versión:** 2.1 | **Fecha de actualización:** 2026-04-27
**Estado:** Validado | **Autor:** Joseph Fernando Gutierrez

---

## 🎯 Criterios de Aceptación Globales
Para que cualquier tarea, módulo o iteración se considere formalmente **finalizada**, debe cumplir estrictamente con los siguientes requisitos transversales:

| # | Criterio | Estándar de Verificación |
|---|---|---|
| 1 | **Integridad del Firmware** | Compilación en entorno de producción sin *warnings*. |
| 2 | **Validación Física** | Superación del protocolo de pruebas industrial correspondiente con registro en `Bitacora_Trazabilidad.csv`. |
| 3 | **Flujo de Git** | Pull Request aprobado y fusionado en `main`. Commits bajo el estándar de [Conventional Commits](https://www.conventionalcommits.org/). |
| 4 | **Revisión de Pares** | Visto bueno técnico por parte del asesor (Prof. Jorge luis Chavez) o miembros del equipo. |
| 5 | **Sincronización Kanban** | Tarea en estado "Done" en GitHub Projects con documentación de evidencia adjunta (CSV/Logs/Fotos). |

---

## 🛠️ Criterios Técnicos Específicos

### 1. Firmware & Adquisición (FW)
Se garantiza la estabilidad del sistema embebido y la confiabilidad de la captura de señales cinemáticas.

| Ref | Requisito Técnico | Parámetro de Éxito | Estado |
|---|---|---|:---:|
| **FW-01** | **Precisión Temporal** | Tasa de muestreo de 100Hz constante mediante **ISR (Interrupt Service Routine)**. Jitter (σ) < 1ms. | ✅ |
| **FW-02** | **Detección de Eventos** | Algoritmo de trigger por *Jerk* calibrado (> 50 m/s³) para inicio automático de grabación. | ✅ |
| **FW-03** | **Gestión de Memoria** | Implementación de **Buffer RAM circular** para evitar bloqueos durante la escritura en SD. | ✅ |

### 2. Hardware & Integración Mecánica (HW)
Se valida la resistencia, el ajuste y el diseño electrónico del prototipo mínimo viable (PMV).

| Ref | Requisito Técnico | Parámetro de Éxito | Estado |
|---|---|---|:---:|
| **HW-01** | **Ajuste Mecánico** | Chasis Sled (PETG) con **O-Rings de compresión** instalados. Ajuste sin vibración radial. | ✅ |
| **HW-02** | **Dimensionamiento** | Ancho máximo de PCB ≤ 20mm para inserción en jabalina estándar (Ø 24mm). | ✅ |
| **HW-03** | **Estabilidad de Voltaje** | Capacitores de desacoplo (100µF/0.1µF) instalados en línea VCC de la SD para mitigar picos de consumo. | ✅ |

### 3. Sistema Integrado & Operación (MC)
Evaluación del desempeño del sistema completo en condiciones reales de uso deportivo.

| Ref | Requisito Técnico | Parámetro de Éxito | Estado |
|---|---|---|:---:|
| **MC-01** | **Autonomía** | Operación continua ≥ 6 horas (Batería Li-Ion 14500). Resultado obtenido: **7h 15m**. | ✅ |
| **MC-02** | **Trazabilidad de Datos** | Archivos CSV generados con estructura legible, sin huecos (gaps) y listos para procesar en MATLAB. | ✅ |
| **MC-03** | **Feedback de Usuario** | Sistema de alertas sonoras (Buzzer) funcional para indicar: Inicializado, Calibrado y Grabación Exitosa. | ✅ |

---

## 🛑 Lo que NO es "Done"
Una tarea se considera incompleta si presenta alguna de las siguientes condiciones:

- ❌ Código que no ha sido probado en el hardware real (ESP32-C3 / BNO055).
- ❌ Mejoras que no cuentan con un reporte de resultados en la bitácora técnica.
- ❌ Hardware ensamblado sin protecciones contra vibraciones (O-Rings).
- ❌ Firmware con retardos (`delay()`) que bloqueen la frecuencia de muestreo de 100Hz.
