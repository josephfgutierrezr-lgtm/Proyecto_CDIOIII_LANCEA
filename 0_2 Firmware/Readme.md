# ⚡ Firmware LANCEA (ESP32 Core)

Este directorio contiene el código fuente C++ para el microcontrolador XIAO ESP32C3. El firmware implementa la lógica de adquisición de datos de alta velocidad, gestión de almacenamiento y transmisión inalámbrica bajo una arquitectura de **Máquina de Estados Finitos (FSM)**.

---

## 🛠️ Entorno de Desarrollo

* **Platform:** PlatformIO (Recomendado) o Arduino IDE.
* **Framework:** Arduino.
* **Board:** `lolin_s2_mini` / `esp32dev` (Ajustar según hardware real).

### Dependencias (Librerías)
Las siguientes librerías son obligatorias para compilar el proyecto:
1.  **Adafruit BNO055** (Driver del sensor IMU).
2.  **Adafruit Unified Sensor** (Base para sensores Adafruit).
3.  **Adafruit SSD1306** (Controlador de Pantalla OLED).
4.  **Adafruit GFX** (Gráficos para pantalla).
5.  **SdFat** (Gestión optimizada de tarjeta SD via SPI).

---

## 🔌 Pinout (Mapa de Conexiones)

Configuración de pines definida en `config.h`:

| Pin XIAO ESP32-C3 | MPU6050 | BNO055 | Buzzer |
| :--- | :---: | :---: | :---: |
| **3V3** | VCC | VCC | -- |
| **GND** | GND | GND | GND |
| **D4 (GPIO6)** | SDA | SDA | -- |
| **D5 (GPIO7)** | SCL | SCL | -- |
| **D3 (GPIO5)** | INT | -- | -- |
| **D6 (GPIO21)** | -- | -- | SIGNAL |
| **GND** | AD0 | ADR | -- |
## 🧠 Lógica del Sistema (Arquitectura)

El sistema no ejecuta un bucle infinito simple. Opera como una **Máquina de Estados** para garantizar la seguridad de los datos.

### Diagrama de Flujo de Estados

```mermaid
stateDiagram-v2
    [*] --> INIT
    INIT --> ERROR : Fallo en Sensor/SD
    ERROR --> [*]
    INIT --> IDLE : Todo OK
    
    IDLE --> ARMADO : Pulsación Corta Botón
    ARMADO --> GRABANDO : Aceleración > 4G (Lanzamiento)
    
    state GRABANDO {
        [*] --> LOGGING
        LOGGING --> LOGGING : 100Hz Loop
    }
    
    GRABANDO --> GUARDADO : Tiempo > 10s o Silencio
    GUARDADO --> IDLE : Archivo Cerrado
    
    IDLE --> WIFI_SYNC : Pulsación Larga Botón (3s)
    WIFI_SYNC --> IDLE : Carga Completa
