# 📂 Gestión del Proyecto LANCEA

Este directorio centraliza la documentación administrativa, planificación y análisis de requisitos del sistema **LANCEA** (Sistema de Monitoreo y Detección de Lanzamiento de Jabalina).

**Institución:** Programa de Ingeniería Electrónica (Septimo Semestre)  
[cite_start]**Ubicación:** Armenia, Quindío, Colombia [cite: 6]  
[cite_start]**Duración:** 2 Semestres (Fase I y II) [cite: 5]

---

## 🎯 Alcance del Proyecto

El objetivo es desarrollar un dispositivo embebido portátil capaz de medir parámetros cinemáticos críticos durante el entrenamiento de lanzamiento de jabalina.

### Objetivos Específicos (KPIs)
1.  [cite_start]**Captura de Aceleración:** Medición en 3 ejes con rango de $\pm16~g$[cite: 9].
2.  [cite_start]**Cálculo de Velocidad:** Estimación de velocidad de salida entre $15~m/s$ y $35~m/s$[cite: 9].
3.  [cite_start]**Estimación de Distancia:** Proyección teórica del tiro entre 35m y 90m[cite: 9].
4.  [cite_start]**Autonomía:** Operación continua $\ge 6$ horas sin recarga[cite: 12].
5.  [cite_start]**Costo:** Presupuesto total entre \$800k y \$1.2M COP[cite: 13].

---

## 📅 Roadmap de Implementación

[cite_start]El proyecto se divide en dos fases semestrales según los lineamientos académicos[cite: 63]:

### Fase 1: Hardware y Firmware Base (Semestre Actual)
| Semanas | Hito / Entregable | Estado |
| :--- | :--- | :--- |
| **1-4** | [cite_start]Adquisición de componentes y Setup inicial del ESP32[cite: 65]. | 🟡 En Progreso |
| **5-8** | [cite_start]Integración de sensores (IMU/Velocidad), detección de evento y Pantalla OLED[cite: 66]. | 🔴 Pendiente |
| **9-12** | [cite_start]Implementación de almacenamiento local (MicroSD/SPIFFS)[cite: 66]. | 🔴 Pendiente |
| **13-16** | [cite_start]Pruebas de campo, calibración de sensibilidad y documentación final[cite: 67]. | 🔴 Pendiente |

### Fase 2: Conectividad y Servidor (Próximo Semestre)
* [cite_start]Despliegue de servidor local (Python/Flask)[cite: 69].
* [cite_start]Sincronización WiFi y Base de Datos[cite: 69, 70].
* [cite_start]Interfaz Web para visualización de historial[cite: 71].

---

## ⚙️ Matriz de Requisitos

### Requisitos Funcionales (RF)
* [cite_start]**RF-001:** Captura de aceleración ($\pm16g$, $\pm0.5~m/s^2$)[cite: 9].
* [cite_start]**RF-002:** Captura de velocidad de lanzamiento[cite: 9].
* [cite_start]**RF-004:** Detección automática del evento de lanzamiento (Sensibilidad $\ge90\%$)[cite: 9].
* **RF-005:** Almacenamiento local ("Black Box") para mín. [cite_start]30 lanzamientos[cite: 10].
* [cite_start]**RF-006:** Transmisión asíncrona ("Store & Forward") al servidor[cite: 10].
* [cite_start]**RF-007:** Visualización inmediata de resultados en pantalla OLED[cite: 10].

### Requisitos No Funcionales (RNF)
* [cite_start]**RNF-003 Portabilidad:** Peso total $\le 1.5$ kg e integración aerodinámica[cite: 12].
* [cite_start]**RNF-005 Resistencia Ambiental:** Operación en clima de Armenia ($15^\circ C - 35^\circ C$, Humedad 60-95%)[cite: 12, 17].
* [cite_start]**RNF-012 Recuperabilidad:** Sistema "Offline-First" ante fallos de red WiFi[cite: 13].

---

## 💰 Presupuesto y Recursos

[cite_start]**Presupuesto Estimado:** \$800.000 - \$1.200.000 COP[cite: 26].

### Componentes Principales (BOM)
* [cite_start]**Microcontrolador:** ESP32 (Dual Core, WiFi/BT)[cite: 20, 22].
* **Sensores:** IMU BNO055 (Acelerómetro + Giroscopio). [cite_start]*Nota: Se utiliza IMU para cálculo de velocidad debido a limitaciones físicas del ultrasonido HC-SR04 en distancias >4m[cite: 24].*
* [cite_start]**Energía:** Batería LiPo/Li-Ion (3.7V)[cite: 24].
* **Interfaz:** Pantalla OLED 0.91" (I2C) y Pulsador físico.

---

## ⚠️ Gestión de Riesgos y Restricciones
1.  [cite_start]**Conectividad:** La red WiFi en estadios no es garantizada. Se mitiga con almacenamiento en SD (RF-005)[cite: 19].
2.  [cite_start]**Clima:** La alta humedad de Armenia requiere protección IP54 o uso de Silica Gel en la carcasa[cite: 58].
3.  [cite_start]**Vibración:** El impacto de la jabalina requiere amortiguación interna en el chasis impreso en 3D[cite: 28].

---
*Documento basado en la especificación de requisitos v1.0 (Octubre 2025).*
