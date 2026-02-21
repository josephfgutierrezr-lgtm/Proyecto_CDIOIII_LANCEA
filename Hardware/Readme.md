# 🔧 Diseño de Hardware y Aviónica - LANCEA

Este directorio documenta la arquitectura electrónica, el diseño de PCB y la integración mecánica del sistema LANCEA. El hardware está diseñado bajo restricciones de **aerodinámica** (factor de forma cilíndrico <22mm) y **resistencia a impactos** (fuerzas >15g).

---

## 📐 Vista General del Dispositivo

El sistema se compone de una **PCB tipo "Strip" (Regla)** de doble cara montada sobre un chasis amortiguado ("Sled") impreso en 3D.

![Render del Dispositivo]([render_preview png](https://github.com/user-attachments/assets/35435e63-3988-4843-8b94-5bf8a7de0638)


### Especificaciones Físicas
* **Dimensiones PCB:** 110mm x 20mm.
* **Diámetro del Chasis (Sled):** 24mm (ajustable según jabalina).
* **Peso Total (con batería):** ~45g.
* **Centro de Gravedad:** Ajustado al eje longitudinal para no alterar el vuelo.

---

## ⚡ Diagrama de Arquitectura

El sistema utiliza una arquitectura de bus dual (I2C + SPI) para separar la adquisición de sensores (baja latencia) del almacenamiento masivo.

```mermaid
graph TD
    BMS[TP4056<br>Carga y Protección] --- BAT[Batería Li-ion 18650<br>3.7V / 2800mAh]
    BAT --> SW[Interruptor]
    SW --> LED[LED ESTADO ON]
    LED --> ESP32[MCU:<br>XIAO ESP32C3<br>3.3V logging]
    
    subgraph I2C Bus [Sensores]
        ESP32 -- GPIO 6/7 --> BNO[IMU:<br>BNO055 / MPU6050<br>Acelerómetro + Giroscopio]
    end
    
    subgraph SPI Bus [Almacenamiento]
        ESP32 -- VSPI --> SD[Módulo MicroSD<br>Logging de Datos]
    end
    
    subgraph Interfaz Fisica [Interfaz Física]
        BTN[Pulsador] -- GPIO 4 --> ESP32
        ESP32 -- GPIO 2 --> Buzzer[Buzzer]
    end
