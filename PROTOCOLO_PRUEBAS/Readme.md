# 🧪 Protocolos de Prueba y Validación (Test Reports)

Este directorio contiene los reportes oficiales de pruebas ejecutadas para el proyecto **LANCEA**. Todas las validaciones siguen los estándares de calidad industrial exigidos en el curso, eliminando la subjetividad y basando los resultados en **datos medibles y tolerancias exactas**.

> 📊 **Documento Oficial:** [Descargar Protocolo de Pruebas Completo (Excel)](./Protocolo_Pruebas_LANCEA.xlsx)

---

## 📌 Resumen Ejecutivo de Pruebas (Fase Actual)

A continuación, se presenta el estado de los últimos test de integración (Hardware, Firmware y Mecánica) correspondientes a la etapa de prototipado inicial:

| ID Prueba | Subsistema | Objetivo Principal | Resultado Medido | Estado |
| :--- | :--- | :--- | :--- | :---: |
| **TEST-HW-01** | PCB (KiCad) | Validar tolerancia dimensional para encaje tubular. | Ancho virtual de baquelita: **19.8mm** (Tolerancia: < 20mm). | ✅ **PASS** |
| **TEST-FW-01** | IMU (MPU6050) | Validar algoritmo de inclinación estática a 45°. | Lectura Serial estable entre **44.5° y 45.1°**. | ✅ **PASS** |
| **TEST-HW-02** | Energía (14500) | Medir autonomía real del sistema en operación. | Tiempo de operación continua: **7 horas y 15 minutos**. | ✅ **PASS** |
| **TEST-MC-01** | Jabalina | Inspección del diámetro interno del tubo deportivo. | Diámetro útil medido con calibrador: **25.2mm**. | ✅ **PASS** |

---

## ⚙️ Metodología de Validación (Definition of Done)

Para que una prueba sea marcada como `✅ PASS` y el componente pase a la columna "Done" en nuestro tablero, debe cumplir estrictamente con los siguientes pilares:

1. **Cero Subjetividad:** No se aceptan descripciones como *"funcionó bien"* o *"la batería duró harto"*. Se exigen valores numéricos (Voltios, Milímetros, Grados, Milisegundos).
2. **Setup Documentado:** Cada prueba en el Excel detalla los instrumentos utilizados (Multímetro Fluke, Calibrador Pie de Rey, Monitor Serial, etc.).
3. **Criterios de Aceptación Predefinidos:** El "Resultado Esperado" se define antes de energizar el circuito, basándose en la hoja de datos (Datasheet) o las restricciones mecánicas.

---
*Documento mantenido por: Joseph Gutierrez - Ingeniería Electrónica*
