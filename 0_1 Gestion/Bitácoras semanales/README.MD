# 🚀 LANCEA  
### Sistema de Telemetría Inteligente para Jabalina

![Estado](https://img.shields.io/badge/Estado-En%20Desarrollo-blue)
![Versión](https://img.shields.io/badge/Versión-2.0-green)
![Plataforma](https://img.shields.io/badge/ESP32-C3-red)
![Licencia](https://img.shields.io/badge/Licencia-Académico-lightgrey)

---

## 🧠 Descripción del Proyecto

**LANCEA** es un sistema de telemetría diseñado para analizar lanzamientos de jabalina en tiempo real, permitiendo medir variables como aceleración, ángulo y potencia.

El sistema integra:
- ⚡ Hardware embebido (ESP32 + IMU)
- 📡 Comunicación WiFi
- 📊 Visualización de datos en PC
- 🧪 Análisis técnico del rendimiento deportivo

---

## ⚙️ Arquitectura del Sistema

```mermaid
graph TD
    A[Sensor IMU BNO055] --> B[ESP32-C3]
    B --> C[WiFi / Serial]
    C --> D[App LANCEA]
    D --> E[Análisis y KPIs]
