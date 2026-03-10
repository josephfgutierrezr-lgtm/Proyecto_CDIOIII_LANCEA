# 🚀 LANCEA - Emulador de Sistemas Dinámicos

![Estado: En Desarrollo](https://img.shields.io/badge/Estado-En_Desarrollo-yellow)
![Hardware: ESP32](https://img.shields.io/badge/Hardware-ESP32-blue)
![Fase: Semanas_7_8](https://img.shields.io/badge/Fase-Semanas_7_a_8-orange)

**Autor:** Joseph Fernando Gutierrez  
**Programa:** Ingeniería Electrónica - Proyecto CDIO III  

LANCEA es un sistema embebido diseñado para la emulación de sistemas dinámicos. Este repositorio contiene el código fuente (Firmware), el diseño de hardware y la documentación técnica correspondiente al desarrollo del Prototipo Mínimo Viable (PMV).

## 📑 Tabla de Contenidos
- [Tecnologías Utilizadas](#-tecnologías-utilizadas)
- [Requisitos de Entrega (PMV)](#-requisitos-de-entrega-pmv)
- [Cronograma de Ejecución](#-cronograma-de-ejecución)
- [Estructura del Repositorio](#-estructura-del-repositorio)

---

## 🛠️ Tecnologías Utilizadas
- **Microcontrolador:** ESP32
- **Validación y Análisis:** MATLAB / Simulink
- **Lenguaje Core:** C/C++
- **Diseño de Hardware:** PCB Definitiva y Modelado 3D

---

## ⚠️ Requisitos de Entrega (PMV)
Estado actual de los entregables obligatorios para la sustentación final:

- [x] **Gestión:** Cronograma actualizado y metodologías de trabajo en equipo.
- [ ] **Hardware:** Circuitos impresos (PCB) definitivos e integrados en chasis electromecánico.
- [ ] **Firmware:** Código fuente estable con manejo de dependencias.
- [ ] **Dossier de Ingeniería:** - [ ] Protocolos de pruebas unitarias y de sistema.
  - [ ] Planos electrónicos y mecánicos.
  - [ ] Manual de usuario y matriz de cumplimiento.

---

## 📊 Cronograma de Ejecución

El siguiente diagrama detalla el plan de trabajo semestral ajustado a las fechas de evaluación obligatorias, abarcando desde el inicio de clases hasta el cierre definitivo en la **Semana 16**.

> **Nota:** La línea vertical roja indica la fecha actual.

```mermaid
gantt
    title Plan de Proyecto LANCEA - Semestre 2026-I
    dateFormat  YYYY-MM-DD
    axisFormat  %d/%m
    todayMarker on

    section Fase 1: Diseño Inicial
    Análisis y Re-Ingeniería      :done,    des1, 2026-02-02, 14d
    Compra de Componentes         :done,    des2, 2026-02-16, 7d
    Diseño Pinout y Diagramas     :done,    des3, 2026-02-23, 7d
    Entrega Portafolio 1 (Sem 5)  :milestone, done, m1, 2026-03-02, 0d

    section Fase 2: Desarrollo
    Pruebas Unitarias de Hardware :done,    dev1, 2026-03-02, 14d
    Desarrollo Firmware ESP32     :active,  dev2, 2026-03-16, 14d
    Fabricación PCB Definitiva    :active,  dev3, 2026-03-16, 14d
    Eval. Proyecto (Sem 9)        :milestone, m2, 2026-03-30, 0d

    section Fase 3: Integración
    Ensamblaje PCB y Chasis 3D    :         int1, 2026-03-30, 14d
    Pruebas de Usabilidad         :         int2, 2026-04-13, 14d
    Cierre de Desarrollo (Sem 13) :milestone, m3, 2026-04-27, 0d

    section Fase 4: Sustentación
    Presentación Cliente (Sem 14) :crit, milestone, m4, 2026-05-04, 0d
    Sustentación Final (Sem 15)   :crit, milestone, m5, 2026-05-11, 0d
    Ajustes y Modificaciones      :         doc1, 2026-05-04, 21d
    Cierre Definitivo (Sem 16)    :milestone, m6, 2026-05-25, 0d
