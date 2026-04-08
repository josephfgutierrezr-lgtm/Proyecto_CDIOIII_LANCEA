# 🛒 Lista de Materiales (Bill of Materials - BOM)

Este documento detalla todos los componentes electrónicos, electromecánicos, pecrios y materiales de manufactura necesarios para ensamblar **una (1) unidad** del sistema **LANCEA**.

> 📄 **Versión Imprimible:** [Descargar BOM Completo en PDF]

---

## ⚡ Electrónica Principal
En esta sección se listan los componentes encargados del procesamiento, adquisición y visualización de datos, estos elementos constituyen el núcleo funcional del sistema, permitiendo la medición, almacenamiento y gestión de la información durante el lanzamiento.

| Ítem | Componente | Cant. | Referencia / Especificación | Función | Est. Costo (COP) |
| :--- | :--- | :---: | :--- | :--- | :---: |
| 1 | **Microcontrolador** | 1 | **ESP32-S2 Mini** (o ESP32-C3) | Procesamiento y WiFi | $ 25.000 |
| 2 | **IMU (Sensor)** | 1 | **Adafruit BNO055** (o genérico) | Acelerómetro + Giroscopio 9-DOF | $ 120.000 |
| 3 | **Pantalla** | 1 | **OLED 0.91"** I2C (128x32) | Interfaz visual (Blanco/Azul) | $ 15.000 |
| 4 | **Almacenamiento** | 1 | **Módulo MicroSD** (SPI Interface) | Lectura/Escritura de datos | $ 8.000 |
| 5 | **Tarjeta Memoria** | 1 | **MicroSD 16GB** Clase 10 | Almacenamiento masivo | $ 20.000 |

## 🔋 Sistema de Potencia

| Ítem | Componente | Cant. | Referencia / Especificación | Función | Est. Costo (COP) |
| :--- | :--- | :---: | :--- | :--- | :---: |
| 6 | **Batería** | 1 | **Li-Ion 14500** (3.7V ~800mAh) | Fuente de energía principal | $ 18.000 |
| 7 | **Cargador** | 1 | **TP4056** (USB-C con protección) | Gestión de carga segura | $ 3.500 |
| 8 | **Interruptor** | 1 | **Slide Switch** (SPDT Mini) | Encendido/Apagado general | $ 1.000 |
| 9 | **Portapilas** | 1 | Holder para 14500 (PCB Mount) | Soporte físico batería | $ 2.500 |

## 🛠️ Interfaz y Mecánica

| Ítem | Componente | Cant. | Referencia / Especificación | Función | Est. Costo (COP) |
| :--- | :--- | :---: | :--- | :--- | :---: |
| 10 | **Pulsador** | 1 | Tact Switch 6x6mm | Botón de Usuario (Trigger) | $ 500 |
| 11 | **LED Indicador** | 1 | LED 5mm RGB (Cátodo Común) | Feedback de estado | $ 1.000 |
| 12 | **Resistencias** | 3 | 220Ω, 10kΩ (1/4W) | Protección LED y Pull-ups | $ 200 |
| 13 | **PCB / Placa** | 1 | Baquelita Universal Doble Cara | Base del circuito (Cortar a medida) | $ 5.000 |
| 14 | **Filamento 3D** | ~20g | PETG o PLA+ | Material para chasis (Sled) | $ 5.000 |
| 15 | **Varios** | 1 | O-Rings, Cable 30AWG, Estaño | Insumos de montaje | $ 10.000 |

---

## 💰 Resumen de Presupuesto

| Categoría | Subtotal Estimado |
| :--- | :--- |
| Electrónica y Sensores | $ 188.000 |
| Potencia y Energía | $ 25.000 |
| Mecánica e Insumos | $ 21.700 |
| **TOTAL POR UNIDAD** | **$ 234.700 COP** |

*(Precios estimados en mercado local colombiano - MercadoLibre / Electrónicas locales a Feb 2026)*

---

## 📍 Proveedores Recomendados
* **Sensores:** Didácticas Electrónicas, Solar Green.
* **Baterías:** MercadoLibre (Vendedores locales).
* **Impresión 3D:** Lab de la Universidad o Hubs locales.

---
