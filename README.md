# 🎯 Proyecto LANCEA: Jabalina Inteligente (CDIO III)

> 🌐 **¡Descubre la presentación interactiva!** 
> Visita la **[Página Oficial del Proyecto LANCEA](https://josephfgutierrezr-lgtm.github.io/Proyecto_CDIOIII_LANCEA/)** para ver el resumen técnico, la arquitectura del sistema y el equipo de desarrollo.

¡Bienvenidos al repositorio oficial del **Proyecto LANCEA**! 

Este espacio documenta el desarrollo integral de un dispositivo deportivo inteligente enfocado en el atletismo. Aquí encontrarás desde la gestión del proyecto hasta los manuales técnicos, hardware, firmware y el entorno de visualización de datos.

---

## 🚀 ¿Qué es LANCEA?
**LANCEA** es un dispositivo electrónico embebido diseñado para integrarse en una jabalina deportiva. Su propósito principal es capturar, procesar y transmitir datos biomecánicos y cinemáticos en tiempo real durante el lanzamiento. 

Al transformar un implemento deportivo tradicional en una herramienta de análisis de datos, LANCEA busca proporcionar retroalimentación cuantitativa para mejorar la técnica y el rendimiento de los atletas.

## 💡 Motivación y Justificación
El deporte de alto rendimiento exige precisión. Tradicionalmente, el análisis del lanzamiento de jabalina depende de la observación visual o de costosos sistemas de cámaras externas. LANCEA nace de la necesidad de democratizar el acceso a métricas precisas (aceleración, rotación, ángulos de ataque) integrando sensores directamente en el implemento. Esto permite una recolección de datos intrusiva mínima y un análisis de sistemas dinámicos mucho más cercano a la realidad física del atleta.

## 🎯 Objetivos
*   **Monitoreo Preciso:** Capturar datos de movimiento en múltiples ejes de manera continua durante la fase de aceleración y vuelo.
*   **Procesamiento Eficiente:** Integrar hardware de bajo consumo y alto rendimiento capaz de procesar la información sin latencia.
*   **Diseño Ergonómico:** Lograr que la adición del hardware no altere significativamente el centro de masa ni la aerodinámica natural de la jabalina.

## 🛠️ Retos Superados y Logros Técnicos
El desarrollo de hardware embebido para un entorno de alto impacto y velocidad presentó desafíos únicos:

*   **Optimización de Espacio y Peso:** Para mantener la integridad aerodinámica y el balance de la jabalina, el diseño prescindió de módulos de registro de datos en tarjeta SD. Esta decisión fue crucial para priorizar la reducción de peso y optimizar el espacio interno disponible.
*   **Comunicación de Sensores:** Se logró una integración exitosa de la unidad de medición inercial (IMU) BNO055. El núcleo de procesamiento se consolidó utilizando el microcontrolador ESP32-C3 SuperMini, estableciendo una comunicación I2C estable a través de los pines físicos 8 (SDA) y 9 (SCL).

## 📂 Estructura del Repositorio
El proyecto está organizado en las siguientes carpetas principales para separar el hardware, el software y la documentación de gestión:

*   📁 **`0_1 Gestion`**: Contiene toda la documentación administrativa del proyecto, incluyendo actas de reuniones, cronogramas, listas de materiales (BOM), costos y planeación maestra de las fases CDIO.
*   📁 **`0_2 Firmware`**: Código fuente desarrollado en C/C++ para el ESP32-C3 SuperMini. Incluye las librerías y rutinas necesarias para la lectura del IMU BNO055 vía I2C y el procesamiento de los datos inerciales.
*   📁 **`DASHBOARD`**: Archivos y scripts relacionados con la interfaz gráfica o panel de control utilizado para visualizar e interpretar los datos cinemáticos capturados por la jabalina.
*   📁 **`DEFINITION_DONE`**: Documentación sobre los criterios de aceptación (DoD - *Definition of Done*), estableciendo los requisitos de calidad y funcionalidad que debe cumplir cada entregable o módulo del proyecto.
*   📁 **`Hardware`**: Planos electrónicos, esquemas de conexión y diseño de integración física de los componentes, garantizando el balance y peso óptimo sin el módulo SD.
*   📁 **`PROTOCOLO_PRUEBAS`**: Procedimientos, metodologías y registros de validación utilizados para someter el dispositivo a pruebas de impacto, estabilidad de conexión y fiabilidad de captura de datos.
*   📁 **`Plantilla_checklist`**: Formatos y listas de chequeo estandarizadas para el control de calidad durante el ensamblasje del hardware y la revisión del código.

---
*¡Explora los directorios, revisa el código y descubre cómo la electrónica y el deporte se unen en LANCEA!*
