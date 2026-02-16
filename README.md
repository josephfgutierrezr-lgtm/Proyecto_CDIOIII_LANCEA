# Proyecto_CDIOIII_LANCEA
# 🚀 LANCEA: Sistema de Monitoreo Biomecánico para Jabalina

![Status](https://img.shields.io/badge/Status-Prototipo-yellow)
![Platform](https://img.shields.io/badge/Platform-ESP32-blue)
![License](https://img.shields.io/badge/License-MIT-green)

**LANCEA** es un sistema embebido de alto rendimiento diseñado para capturar, analizar y transmitir datos cinemáticos durante el lanzamiento de jabalina. Diseñado para superar las limitaciones de los sensores ópticos tradicionales, LANCEA utiliza **Fusión de Sensores Inerciales (IMU)** para reconstruir la trayectoria del vuelo en entornos donde el GPS o el ultrasonido no son viables.

---

## 🎯 Objetivo del Proyecto

Desarrollar un dispositivo de bajo costo (< $100 USD), ligero y aerodinámico capaz de insertarse en una jabalina de competición para medir:
1.  **Velocidad de Salida ($V_0$):** Mediante integración de aceleración lineal.
2.  **Ángulo de Ataque ($\theta$):** Mediante cuaterniones y ángulos de Euler.
3.  **Estabilidad de Vuelo:** Análisis de rotación (Roll/Yaw).
4.  **Distancia Estimada:** Proyección balística basada en cinemática.

---

## 🛠️ Hardware y Arquitectura

El sistema opera bajo una arquitectura **"Store & Forward"** (Almacenar y Reenviar) para garantizar la integridad de los datos en lanzamientos de larga distancia (>80m).

### Lista de Componentes (BOM)
* **MCU:** ESP32-S2 Mini / ESP32-C3 (Dual Core 240MHz).
* **IMU:** Bosch BNO055 (Acelerómetro + Giroscopio + Magnetómetro + Cortex M0 interno).
* **Almacenamiento:** Módulo MicroSD SPI (Logging a 100Hz).
* **Display:** OLED 0.91" I2C (128x32) para feedback inmediato al atleta.
* **Energía:** Batería Li-Ion 14500 (1000mAh) + BMS TP4056.
* **Chasis:** Diseño cilíndrico impreso en 3D (PETG) con amortiguación de impacto.

### Diagrama de Bloques
`[Sensor BNO055] --(I2C)--> [ESP32] --(SPI)--> [Micro SD]`
`[ESP32] --(WiFi/HTTP)--> [Servidor Python Flask]`

---

## ⚙️ Funcionalidades Clave

### 1. Algoritmo de Detección de Lanzamiento
El sistema permanece en *Deep Sleep* hasta detectar un pico de aceleración **> 4G**, activando el modo de grabación de alta frecuencia.

### 2. Navegación Inercial (Dead Reckoning)
A diferencia de sistemas básicos que usan ultrasonido (limitado a 4m), LANCEA utiliza el vector de gravedad y la aceleración lineal pura del BNO055 para calcular la velocidad en tiempo real sin referencias externas.

### 3. Sincronización WiFi
Al recuperar la jabalina, el usuario presiona un botón físico. El ESP32 activa su radio WiFi, busca el servidor local y descarga los archivos `.csv` del vuelo automáticamente.

---

## 🚀 Instalación y Uso

### Firmware (ESP32)
1.  Clonar el repositorio.
2.  Abrir con **PlatformIO** o **Arduino IDE**.
3.  Instalar librerías: `Adafruit_BNO055`, `Adafruit_SSD1306`, `SdFat`.
4.  Configurar credenciales WiFi en `config.h`.

### Servidor Local (Python)
Para recibir los datos en tu PC:
```bash
cd server
pip install flask
python server.py
