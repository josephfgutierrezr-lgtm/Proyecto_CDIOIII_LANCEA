# 🚀 Definition of Done (DoD) — Proyecto LANCEA
**Versión:** 3.0 (Final) | **Fecha de actualización:** 2026-05-06
**Estado:** Finalizado y Consolidado | **Autor:** Joseph Fernando Gutierrez Reyes

---

## 🎯 Criterios de Aceptación Globales
Todos los módulos e iteraciones han cumplido estrictamente con los siguientes requisitos transversales para su consolidación final:

| # | Criterio | Estándar de Verificación | Estado |
|---|---|---|:---:|
| 1 | **Integridad del Firmware** | Compilación en entorno de producción sin *warnings*. | ✅ |
| 2 | **Validación Física** | Superación del protocolo de pruebas industrial con registro definitivo en `Bitacora_Trazabilidad.csv`. | ✅ |
| 3 | **Flujo de Git** | Pull Requests aprobados y fusionados en `main`. Commits bajo el estándar *Conventional Commits*. | ✅ |
| 4 | **Revisión de Pares** | Visto bueno técnico final por parte del asesor y validación de los miembros del equipo. | ✅ |
| 5 | **Sincronización Kanban** | Todas las tareas en estado "Done" en GitHub Projects con documentación y evidencia de integración adjunta. | ✅ |

---

## 🛠️ Criterios Técnicos Específicos Cumplidos

### 1. Firmware & Adquisición (FW)
Se garantizó la estabilidad del sistema embebido y la confiabilidad de la captura de señales cinemáticas tras las optimizaciones finales.

| Ref | Requisito Técnico | Parámetro de Éxito Alcanzado | Estado |
|---|---|---|:---:|
| **FW-01** | **Precisión Temporal** | Tasa de muestreo de 100Hz constante mediante **ISR (Interrupt Service Routine)**. Jitter (σ) < 1ms. | ✅ |
| **FW-02** | **Detección de Eventos** | Algoritmo de trigger por *Jerk* calibrado (> 50 m/s³) para inicio automático de captura de telemetría. | ✅ |
| **FW-03** | **Gestión de Memoria** | Estructuración de datos optimizada en memoria tras la decisión técnica de remover el módulo de tarjeta SD, reduciendo peso y evitando bloqueos de escritura. | ✅ |

### 2. Hardware & Integración Mecánica (HW)
Se validó la resistencia, el balance del centro de gravedad aerodinámico y el diseño electrónico del prototipo definitivo.

| Ref | Requisito Técnico | Parámetro de Éxito Alcanzado | Estado |
|---|---|---|:---:|
| **HW-01** | **Ajuste Mecánico** | Chasis Sled (PETG) con **O-Rings de compresión** instalados. Ajuste estructural sin vibración radial dentro del tubo. | ✅ |
| **HW-02** | **Dimensionamiento** | Ancho de PCB Strip ≤ 20mm insertada en la jabalina (Ø 24mm). Bus I2C operando correctamente en pines físicos 8 (SDA) y 9 (SCL) del ESP32-C3. | ✅ |
| **HW-03** | **Estabilidad de Voltaje** | Capacitores de desacoplo (100µF/0.1µF) instalados en la línea VCC principal para mitigar picos de consumo entre el microcontrolador y el sensor BNO055. | ✅ |

### 3. Sistema Integrado & Operación (MC)
Desempeño del sistema completo validado en pista, garantizando la recolección de datos y el flujo de energía.

| Ref | Requisito Técnico | Parámetro de Éxito Alcanzado | Estado |
|---|---|---|:---:|
| **MC-01** | **Autonomía y Recarga** | Operación continua validada (> 7 horas continuas). Módulo TP4056 plenamente accesible desde la sección trasera mediante USB-C sin necesidad de desmontar el chasis. | ✅ |
| **MC-02** | **Trazabilidad de Datos** | Paquetes de datos exportados con estructura matricial legible, sin huecos (gaps) y listos para su modelado y análisis en MATLAB. | ✅ |
| **MC-03** | **Feedback de Usuario** | Sistema de alertas sonoras (Buzzer) y visuales (LED de carga) funcional para indicar: Inicializado, Calibrado, Grabación en curso y Estado de Batería. | ✅ |

---

## 🏁 Cierre de Proyecto y Conformidad
El proyecto LANCEA se declara **Terminado y Consolidado**. No existen tareas pendientes, bloqueos técnicos ni implementaciones de hardware/firmware sin validar. Todos los criterios de exclusión históricos (código sin probar dinámicamente, alteraciones del punto de equilibrio, falta de protecciones antivibración o bloqueos por funciones como `delay()`) fueron mitigados satisfactoriamente, culminando en un prototipo funcional y listo para la recolección de datos en campo.
