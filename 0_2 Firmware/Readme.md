# ⚡ Firmware LANCEA (ESP32 Core)

Este directorio contiene el código fuente C++ para el microcontrolador XIAO ESP32C3. El firmware implementa la lógica de adquisición de datos de alta velocidad, gestión de almacenamiento y transmisión inalámbrica bajo una arquitectura de **Máquina de Estados Finitos (FSM)**.

---

## 🛠️ Entorno de Desarrollo
En esta sección se definen las herramientas, plataforma y dependencias necesarias para compilar, cargar y mantener el firmware del sistema, lo cual asegura reproducibilidad en el entorno de desarrollo entre los miembros del equipo.

* **Platform:** PlatformIO (Recomendado) o Arduino IDE.
* **Framework:** Arduino.
* **Board:** `lolin_s2_mini` / `esp32dev` (Ajustar según hardware real).

### Dependencias (Librerías)
Las siguientes librerías son obligatorias para compilar el proyecto y permiten la correcta interacción con los sensores, pantalla y sistema de almacenamiento:
1.  **Adafruit BNO055** (Driver del sensor IMU).
2.  **Adafruit Unified Sensor** (Base para sensores Adafruit).
3.  **Adafruit SSD1306** (Controlador de Pantalla OLED).
4.  **Adafruit GFX** (Gráficos para pantalla).
5.  **SdFat** (Gestión optimizada de tarjeta SD via SPI).

---

## 🔌 Pinout (Mapa de Conexiones)

A continuación se presenta la asignación de pines utilizada en el sistema. Esta configuración está definida en el archivo config.h y es fundamental para garantizar la correcta conexión entre el microcontrolador y los periféricos.

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
En esta sección se describe el comportamiento del firmware a nivel lógico, el sistema no opera mediante un bucle tradicional, sino mediante una Máquina de Estados Finitos (FSM), lo que permite controlar de forma estructurada los eventos, optimizar recursos y garantizar la integridad de los datos durante el proceso de adquisición.

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
