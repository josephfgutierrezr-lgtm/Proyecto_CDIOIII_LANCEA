# 📊 Dashboard MAHD: Estructura y Automatización
**Proyecto:** LANCEA | **Estado:** 100% Validado y Consolidado | **Autor:** Joseph Fernando Gutierrez Reyes

---

## 📋 Descripción General
El **Dashboard MAHD** es la herramienta centralizada de control y seguimiento diseñada para garantizar la integridad, trazabilidad y validación del 100% de la documentación técnica, operativa y de pruebas del proyecto **LANCEA**.

Este tablero consolida los registros de la bitácora técnica, la matriz de requisitos y los criterios de aceptación (Definition of Done), asegurando que cada fase de diseño (Hardware y Firmware) cuente con su respectiva evidencia y validación.

🔗 **[Acceder al Dashboard MAHD - Google Sheets](https://docs.google.com/spreadsheets/d/1KiI5yMVQRohlRCCxRSIlaxDekqpGnXFfwT1b4ooLA6A/edit?gid=1975843790#gid=1975843790)**

---

## 🎯 Objetivos del Dashboard
1. **Validación Exhaustiva:** Certificar que el 100% de los entregables y pruebas de concepto (PoC) documentadas cumplen con los parámetros del proyecto.
2. **Trazabilidad de Componentes:** Mantener el historial de modificaciones estructurales y de código (ej. retiro de SD, integración de Módulo TP4056, migración a ESP32-C3).
3. **Control de Calidad (QA):** Vincular los resultados dinámicos en pista con los parámetros teóricos del simulador.

---

## 🧩 Estructura de la Documentación Validada

El dashboard abarca la validación de las siguientes áreas clave:

### 1. Firmware & Lógica de Adquisición
* [x] Rutinas de interrupción (ISR) y muestreo a 100Hz constante.
* [x] Algoritmos de trigger automático por *Jerk*.
* [x] Optimización de buffer y gestión de memoria interna.
* [x] Verificación de ausencia de retardos bloqueantes (`delay()`).

### 2. Hardware & Mecánica
* [x] Restricciones dimensionales (Ancho PCB ≤ 20mm para tubo Ø 24mm).
* [x] Balance aerodinámico y centro de gravedad de la jabalina.
* [x] Integración de puertos de recarga traseros (USB-C) y gestión de batería Li-Ion.
* [x] Sistema de amortiguación (O-Rings).

### 3. Operación & Integración Continua
* [x] Autonomía energética comprobada (> 7 horas).
* [x] Exportación e integridad de paquetes de datos (matrices listas para MATLAB).
* [x] Cierre y consolidación del *Definition of Done (DoD)* (Versión 3.0 Final).

---

## 🛠️ Instrucciones de Uso y Mantenimiento
Dado que el proyecto ha alcanzado la fase de **Consolidación**, el dashboard operará en modo de **Sólo Lectura / Auditoría**. 
* Cualquier extracción de métricas para la redacción del documento final de grado debe referenciar directamente los KPIs generados en las hojas de cálculo automatizadas.
* Los scripts y macros asociados en el dashboard aseguran la integridad de los datos históricos; no se deben alterar las fórmulas de la matriz principal.

---

