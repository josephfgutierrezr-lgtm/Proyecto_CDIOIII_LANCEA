# Registro Integrado de Retroalimentación, Protocolos de Prueba y Definition of Done (DoD)
**Proyecto:** LANCEA - Sistema de Medición y Emulación para Atletas de Jabalina  
**Cliente / Usuario Final:** Entrenador y Atleta de la Liga de Atletismo del Quindío  
**Ingenieros a Cargo:** Joseph Fernando Gutiérrez, Emerson Santiago Córdoba, Johan Rodrigo Piedrahita

---

## 1. Introducción y Justificación
Este documento detalla cómo las necesidades empíricas y cualitativas del usuario final (entrenador y atleta de jabalina) fueron traducidas en requerimientos técnicos estrictos, historias de usuario medibles y validaciones cuantificables. El propósito de este registro es evidenciar que el desarrollo del dispositivo **LANCEA** siguió una ruta de ingeniería rigurosa (basada en métricas, metodologías ágiles y estándares industriales) descartando la improvisación y garantizando un producto funcional, ergonómico y preciso.

---

## 2. Historias de Usuario: La Voz del Cliente (Feedback)
El proceso de retroalimentación en campo nos permitió capturar las necesidades reales, las cuales fueron formalizadas en la **Matriz de Enfoque y Requisitos**:

* **HU-01 (Entrenador):** *Requiere ver la velocidad y ángulo de lanzamiento para corregir la técnica.* -> Prioridad P0. Define el uso del IMU y el procesamiento inercial.
* **HU-02 (Atleta):** *Exige que el sistema sea invisible dentro de la jabalina para no alterar su vuelo ni ergonomía.* -> Prioridad P0. Define los límites mecánicos del diseño, promoviendo la máxima reducción de peso y volumen.
* **HU-03 (Entrenador/Técnico):** *Necesita descargar datos en CSV sin cables y de forma inmediata para agilizar el análisis.* -> Prioridad P1. Se descartó el almacenamiento físico (memoria micro SD) para evitar problemas de espacio y peso adicional en la jabalina. En su lugar, se definió una arquitectura donde la información se envía y guarda directamente en archivos CSV desde la aplicación y la página web.
* **HU-04 (Investigación):** *Requiere un registro de 100 muestras/segundo para el análisis biomecánico.* -> Prioridad P0. Define la tasa de muestreo, rutinas de interrupción (ISR) y la transmisión estable de datos a la interfaz.
* **HU-05 (Usuario en campo):** *La batería debe durar al menos 6 horas para cubrir un entrenamiento completo.* -> Prioridad P1. Define el sistema de potencia.

---

## 3. Definition of Done (DoD): Estándares de Aceptación
Para asegurar que las decisiones tomadas cumplieran con la calidad exigida y no fueran validaciones subjetivas (ej. "funciona bien"), se estableció un **Definition of Done (DoD)** riguroso:

1.  **Cero Subjetividad:** Todas las validaciones deben arrojar valores numéricos (Voltios, Milímetros, Grados, Milisegundos).
2.  **Firmware (FW) y Software:** 
    * Tasa de muestreo de **100Hz exacta** garantizada por ISR (Interrupt Service Routine) con Jitter < 1ms, evitando el uso de retardos (`delay()`) que bloqueen la lectura.
    * Detección de lanzamiento por **Jerk calibrado (> 50 m/s³)**.
    * Transmisión íntegra de datos vía Wi-Fi (ESP32 como servidor local/AP) hacia la aplicación/página web para la generación automática del archivo CSV, garantizando cero pérdida de paquetes y eliminando la dependencia de hardware de almacenamiento extra (SD).
3.  **Hardware (HW) y Mecánica:** 
    * Ancho máximo de la PCB **≤ 20mm**.
    * Eliminación del módulo SD y sus componentes asociados, reduciendo drásticamente el peso y volumen final.
    * Uso de **O-Rings de compresión** en el chasis (Sled) de PETG para evitar vibración radial e impactos.
4.  **Sistema e Interacción (MC):** 
    * Feedback al usuario mediante **Buzzer** (alertas sonoras para encendido, calibración y conexión/grabación exitosa), solucionando la necesidad de interacción rápida.

---

## 4. Ejecución de Pruebas Industriales (Verificación de Requisitos)
Las historias de usuario y el DoD se validaron mediante los siguientes protocolos de prueba documentados, a cargo del ingeniero Joseph Gutierrez:

### 🛠️ Prueba Mecánica y Dimensional (TEST-MC-01 & TEST-HW-01)
* **Problema del Atleta (HU-02):** El dispositivo debe encajar perfectamente sin estorbar y ser lo más ligero posible.
* **Protocolo:** Se midió el diámetro interno de una jabalina profesional con calibrador Pie de Rey, obteniendo **25.2mm** (TEST-MC-01). 
* **Validación de PCB:** Gracias a la eliminación de la memoria SD, se optimizó la baquelita en KiCad definiendo un límite estricto. La medición final del ancho de la placa fue de **19.8mm** (TEST-HW-01). 
* **Resultado:** ✅ **PASS**. Se garantiza el encaje aerodinámico perfecto y se minimiza el peso añadido al implemento.

### 🔋 Prueba de Autonomía de Potencia (TEST-HW-02)
* **Problema del Usuario (HU-05):** El sistema debe durar una sesión de 6 horas.
* **Protocolo:** Se testeó una batería Li-Ion 14500 (1000mAh) con el ESP32 en modo activo continuo, transmitiendo datos vía web/app hasta el corte del BMS (3.0V).
* **Resultado:** ✅ **PASS**. El sistema operó ininterrumpidamente por **7 horas y 15 minutos**, superando holgadamente la exigencia.

### 📐 Prueba de Calibración Inercial (TEST-FW-01)
* **Problema del Entrenador (HU-01):** Confianza en los ángulos reportados en el archivo CSV generado.
* **Protocolo:** Uso de escuadra física a 45° en estático. La interfaz web/app debía registrar el ángulo con un error máximo de ±2°.
* **Resultado:** ✅ **PASS**. Lectura estable entre **44.5° y 45.1°**.

---

## 5. Conclusión: Trazabilidad del Proyecto
El cruce entre los comentarios del cliente, la Matriz de Requisitos, el Definition of Done y el Protocolo de Pruebas demuestra una **trazabilidad completa y profesional**. Cada decisión de diseño —como la transmisión y generación remota de archivos CSV para prescindir del módulo SD y alivianar el peso, la implementación de ISR a 100Hz, alertas sonoras con Buzzer, y el dimensionamiento estricto a 19.8mm de la PCB— se fundamentó directamente en los comentarios del entrenador y el atleta.

Se evidencia que LANCEA no es el resultado de la experimentación empírica, sino de un proceso sistemático de ingeniería que asegura confiabilidad, precisión de datos y usabilidad en el entorno real de alto rendimiento deportivo del Quindío.
