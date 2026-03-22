# 🧠 LANCEA Firmware: Explicación del Código (`LANCEA_WiFi.ino`)

Este documento explica la lógica interna del firmware principal del proyecto LANCEA, diseñado para el microcontrolador XIAO ESP32-C3. 

El objetivo principal de este código es **capturar datos inerciales a alta velocidad (100 Hz)** durante el breve instante que dura un lanzamiento de jabalina, sin perder información, y luego disponibilizar esos datos a través de una red WiFi local.

---

## 🏗️ 1. Arquitectura de Captura: El método "Store & Forward"

El mayor desafío técnico de este código es la velocidad. Escribir datos por WiFi o en una memoria física toma tiempo (milisegundos) y bloquearía el microcontrolador, arruinando la frecuencia de muestreo de 100 Hz. 

Para solucionar esto, el código utiliza una arquitectura **Store and Forward (Almacenar y Transmitir)**:
1. **Store (RAM):** Durante el lanzamiento, los datos del sensor BNO055 se guardan temporalmente en la memoria RAM ultra-rápida del ESP32 (usando arrays o un buffer).
2. **Forward (Web/Serial):** Una vez que el lanzamiento termina y la jabalina está en vuelo/caída, el ESP32 toma esos datos de la RAM y los formatea como un archivo CSV para enviarlos a la aplicación o al servidor web.

---

## 🔄 2. La Máquina de Estados del Lanzamiento

El `loop()` principal no ejecuta todo el código a la vez. Funciona como una máquina de estados que reacciona a los movimientos del atleta:

* **ESTADO 0: Reposo (IDLE)**
    * El sensor BNO055 está tomando lecturas constantemente.
    * El código calcula el **Jerk** (la derivada de la aceleración, es decir, qué tan rápido cambia la aceleración).
    * Si el Jerk supera el límite configurado (`JERK_THRESHOLD`), significa que el atleta acaba de iniciar el impulso explosivo. El sistema salta al Estado 1.

* **ESTADO 1: Captura Activa (RECORDING)**
    * El LED del microcontrolador se enciende fijo.
    * Se inicia un temporizador. Durante un tiempo predefinido (ej. 2 o 3 segundos de la ventana de lanzamiento), el sistema guarda la aceleración (X, Y, Z) y la orientación a exactamente 100 Hz en la memoria RAM.
    * Se ignora cualquier conexión WiFi entrante para no interrumpir la captura.

* **ESTADO 2: Procesamiento y Envío (DONE)**
    * El LED parpadea rápidamente 3 veces.
    * El sistema vuelve a habilitar el servidor WiFi.
    * Los datos están listos para ser descargados desde el portal `192.168.4.1` o enviados por el puerto Serial (comando `DUMP`).
    * El sistema vuelve al ESTADO 0 esperando el siguiente lanzamiento.

---

## 📡 3. El Servidor Web Integrado (Access Point)

El ESP32 no necesita un router externo. El código configura el microcontrolador en modo **Access Point (AP)**:
* **SSID:** `LANCEA_AP`
* **IP:** `192.168.4.1`

Utiliza la librería `WebServer.h` (o `AsyncWebServer`) para enrutar las peticiones HTTP:
* `GET /`: Sirve la página principal en HTML (alojada en la memoria del código mediante PROGMEM o SPIFFS) donde se ven los lanzamientos.
* `GET /atletas`: Maneja el registro y selección del atleta activo.
* `GET /download`: Empaqueta el buffer de RAM en un formato `.csv` y lo envía al navegador del teléfono o PC.

---

## ⚙️ 4. Variables Clave para Calibración

Si necesitas ajustar el comportamiento del dispositivo en campo, busca estas variables al inicio del código:

| Variable | Función | Cuándo modificarla |
| :--- | :--- | :--- |
| `JERK_THRESHOLD` | Nivel de sacudida necesario para iniciar a grabar. | Súbelo si hay "falsos positivos" al caminar. Bájalo si no detecta el lanzamiento. |
| `SAMPLE_RATE` o `DELAY` | Frecuencia de captura (típicamente 10ms para 100Hz). | Mantener en 10ms. Modificar solo si cambias el sensor. |
| `RECORD_TIME` | Cuántos milisegundos graba después de detectar el Jerk. | Auméntalo si el vuelo de la jabalina se corta en los datos. |
| `DEBUG_MODE` | Imprime datos extra por el Monitor Serial. | Ponlo en `1` para calibrar el Jerk en el escritorio. Ponlo en `0` para usar en campo. |

---

## 🛠️ 5. Dependencias y Librerías

Para compilar este código en Arduino IDE, asegúrate de tener instaladas:
* `WiFi.h` y `WebServer.h` (Nativas del paquete ESP32)
* `Wire.h` (Para comunicación I2C)
* `Adafruit_BNO055` y `Adafruit_Sensor` (Para procesar los cuaterniones del IMU).

---
*Desarrollado para el análisis cinemático de jabalina.*
