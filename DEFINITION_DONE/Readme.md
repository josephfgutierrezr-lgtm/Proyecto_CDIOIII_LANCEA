# Criterios de Aceptación y Definition of Done (DoD) - LANCEA

Esta matriz define los atributos funcionales, físicos y de rendimiento exactos que cada componente debe cumplir para ser considerado como "Terminado" (Done) en el tablero Kanban.

| Módulo / Componente | Criterio de Aceptación (El Atributo) | Métrica / Tolerancia Exacta (El DoD) |
| :--- | :--- | :--- |
| **Hardware:** Módulo de Potencia (Batería 14500 + TP4056) | Regulación de Voltaje y Autonomía | Salida analógica hacia el ESP32 estable entre **3.2V y 3.4V**. Capacidad de mantener el sistema encendido en modo de grabación continua por **≥ 6 horas**. |
| **Hardware:** PCB y Ruteo | Integridad de Señal (Buses I2C/SPI) | Cero interferencias o reinicios durante la operación del motor I2C a **400 kHz** (BNO055) y SPI a **4 MHz** (MicroSD). |
| **Firmware:** Adquisición IMU (BNO055) | Rendimiento / No-blocking | Tiempo de ejecución del ciclo de lectura de aceleración y cuaterniones **< 10ms**. Cero uso de la función `delay()`. |
| **Firmware:** Datalogger (MicroSD) | Velocidad de Escritura (Throughput) | Capacidad de escribir archivos `.csv` a una frecuencia estable de **100 Hz** (100 muestras por segundo) con **0% de pérdida de tramas** (dropped frames). |
| **Firmware:** Algoritmo de Trigger | Precisión de Detección de Evento | El sistema debe pasar del estado `ARMADO` a `GRABANDO` en menos de **50 ms** tras detectar una aceleración lineal en el eje longitudinal **> 4g**. |
| **Mecánica:** Chasis Impreso (Sled) | Tolerancia de Ensamble Dimensional | La PCB tipo "Strip" (20mm) debe encajar en los rieles del cilindro con una holgura máxima de **±0.5mm**, sin requerir fuerza que flexione la baquelita. |
| **Mecánica:** Resistencia al Impacto | Resistencia Mecánica en Aterrizaje | Las soldaduras y anclajes de la batería deben soportar picos de desaceleración brusca sin presentar desconexiones (falsos contactos). |
| **Gestión:** Repositorio GitHub | Calidad y Trazabilidad de Código | **0 Errores** y **0 Warnings** de compilación. Código subido a la rama `main` con commit trazable usando palabra clave (`Closes #ID`). |
