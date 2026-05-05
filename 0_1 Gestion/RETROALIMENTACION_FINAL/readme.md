# Validación Final y Entrega del Producto LANCEA

**Proyecto:** LANCEA - Sistema de Medición y Emulación para Atletas de Jabalina  
**Cliente / Usuario Final:** Entrenador y Atleta de la Liga de Atletismo del Quindío  
**Ingenieros a Cargo:** Joseph Fernando Gutiérrez, Emerson Santiago Córdoba, Johan Rodrigo Piedrahita  
**Fecha de Entrega:** Mayo 2026

---

## 1. Resumen de Entrega
Este documento oficializa la culminación y entrega del proyecto **LANCEA**. Tras un ciclo de desarrollo iterativo basado en la metodología CDIO (Concebir, Diseñar, Implementar, Operar), el sistema ha pasado de ser un concepto a una herramienta tecnológica validada y funcional en un entorno real de alto rendimiento. Las pruebas de campo y la retroalimentación final del cliente confirman el éxito rotundo de la implementación.

## 2. Pruebas de Campo Reales (Operación)
Las pruebas finales se ejecutaron en la pista de atletismo con la participación directa del entrenador y un atleta de la Liga del Quindío, sometiendo el dispositivo a condiciones reales de entrenamiento.

### 2.1. Condiciones de Prueba
* **Entorno:** Pista de atletismo al aire libre.
* **Implemento:** Jabalina profesional con el dispositivo LANCEA integrado.
* **Procedimiento:** El atleta realizó múltiples secuencias completas de lanzamiento (carrera de aproximación, cruce y liberación) a máxima intensidad.
* **Captura de Datos:** El dispositivo registró y transmitió los datos inerciales (ángulos, velocidad, aceleración) de forma inalámbrica a la interfaz web/app a pie de pista.

### 2.2. Resultados de la Validación Técnica
* **Integridad Física:** El hardware (PCB de 19.8mm, encapsulado) soportó las fuerzas G y las vibraciones extremas del impacto de la jabalina contra el suelo sin sufrir daños estructurales, gracias al diseño con O-Rings de compresión.
* **Estabilidad Dinámica:** Se comprobó que el peso y la ubicación del dispositivo no alteraron el centro de gravedad ni la parábola de vuelo natural de la jabalina.
* **Transmisión Inalámbrica:** El envío de datos desde el ESP32 (funcionando como Access Point) hacia la interfaz generó archivos CSV precisos en tiempo real, validando la eliminación de la tarjeta SD y demostrando robustez en un entorno sin internet.

## 3. Retroalimentación Final del Cliente (La Voz del Usuario)
La evaluación cualitativa del usuario final es el indicador definitivo del éxito de LANCEA. Las opiniones recopiladas durante la entrega destacan el impacto del producto:

* **Atleta:** *"El dispositivo es prácticamente imperceptible. No tuve que modificar mi agarre ni sentí que el peso afectara la trayectoria. El sonido de confirmación (Buzzer) me ayudó a saber exactamente cuándo estaba listo para lanzar, sin interrumpir mi concentración."*
* **Entrenador:** *"Por fin tenemos datos objetivos e inmediatos. Poder descargar el CSV en la misma pista sin depender de cables o de una red Wi-Fi externa es un cambio total en la dinámica de entrenamiento. Los ángulos registrados coinciden con las correcciones biomecánicas que necesitamos hacer."*

## 4. Evidencia Multimedia
Para respaldar este hito, se adjuntan los siguientes archivos en el repositorio:
* `PRUEBA_CAMPO_REAL.jpeg`: Registro fotográfico del atleta en posición de lanzamiento con el dispositivo LANCEA.
* `PRUEBA_CAMPO_REAL_2.jpeg`: Captura del dispositivo integrado en la jabalina durante la fase de preparación.
* `COMENTARIOS_LANCEA.mp4`: Material audiovisual con las declaraciones y opiniones de primera mano del entrenador y el atleta tras utilizar el sistema.

## 5. Cierre de Proyecto
Con la validación técnica en campo y la aprobación entusiasta del cliente, el equipo de ingeniería declara el proyecto **LANCEA** como exitosamente entregado. El producto cumple a cabalidad con la Matriz de Requisitos, el Definition of Done y soluciona un problema latente en el entrenamiento deportivo regional de forma profesional e innovadora.
