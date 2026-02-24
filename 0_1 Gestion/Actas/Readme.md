# 📂 Actas y Evolución de Planeación

Este directorio contiene los documentos maestros de gestión, auditoría y planeación del proyecto **LANCEA**. 

Para garantizar la **trazabilidad** de las decisiones de ingeniería, se mantienen las diferentes versiones de la matriz de planeación. Esto permite visualizar cómo el proyecto evolucionó desde los supuestos teóricos iniciales hasta las especificaciones técnicas basadas en pruebas físicas reales.

---

## 📄 Documentos Disponibles

### 1. 🛑 VERSIÓN 1: Línea Base Teórica (`v1_Planeacion_Inicial`)
Corresponde a la planeación del semestre anterior y las primeras fases de ideación. 
* **Característica:** Basada en supuestos teóricos y componentes genéricos.
* **Estado:** Obsoleta (Solo para fines de trazabilidad y auditoría).

### 2. ✅ VERSIÓN 2: Planeación Maestra Actualizada (`v2_Planeacion_Maestra`)
Corresponde a la realidad técnica actual (Semana 3 en adelante) tras ejecutar la auditoría de diseño y las primeras pruebas de concepto (PoC).
* **Característica:** Basada en validaciones físicas, medidas reales y componentes definitivos adquiridos.
* **Estado:** **ACTIVA** (Documento rector del proyecto).

---

## 🔄 Changelog Técnico: ¿Qué cambió de V1 a V2?

La transición hacia la V2 fue impulsada por restricciones físicas (tamaño) y de rendimiento descubiertas en laboratorio. Los cambios más críticos son:

| Subsistema | En la Versión 1 (Ideación) | En la Versión 2 (Realidad Actual) | Justificación del Cambio |
| :--- | :--- | :--- | :--- |
| **Sensores** | MPU6050 + Ultrasónico | **Solo IMU BNO055** | El ultrasonido no tiene alcance útil (>4m) y daña la aerodinámica. El BNO055 entrega cuaterniones por hardware, evitando el "Gimbal Lock". |
| **Control** | ESP32 DevKit V1 | **ESP32-S2 / C3 Mini** | El DevKit estándar (28mm) no cabe en el tubo de la jabalina (25.2mm). |
| **Energía** | Batería LiPo Plana | **Li-Ion Cilíndrica 14500** | La 14500 (14mm diámetro) permite un ensamble tubular perfecto en el "Sled" 3D y otorgó >7h de autonomía probada. |
| **Interfaz** | Pantalla OLED | **Buzzer + LED de Estado** | Eliminación de OLED por consumo energético y espacio. El Buzzer brinda mejor feedback auditivo en campo abierto. |
| **Almacenaje**| Transmisión WiFi Directa | **Módulo MicroSD (SPI)** | El cuerpo de aluminio de la jabalina actúa como Jaula de Faraday. Se prioriza el guardado local (Data Logging). |
| **Riesgo** | Alteración del Centro de Gravedad | **Impacto Físico (>15g)** | El riesgo principal ahora es la desconexión o corrupción de la memoria SD por el impacto al clavar la jabalina en el suelo. |

---

## 🔍 Notas de Auditoría (Definition of Done)
Todos los componentes de la **V2** están sujetos a las métricas estrictas definidas en nuestro archivo de *Protocolos de Prueba*, asegurando que el paso a la columna "Terminado" se base en datos y no en suposiciones.

*Documento gestionado por: Joseph Gutierrez - Líder de Proyecto*
