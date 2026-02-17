# 📅 Cronograma de Ejecución - Proyecto LANCEA

Este documento detalla el plan de trabajo semestral, el seguimiento de hitos y el estado actual del desarrollo del sistema.

**Estado Actual:** 🟡 Semana 3 (En Ejecución)  
**Fase:** Prototipado Inicial y Pruebas Unitarias  
**Semestre:** 2026-I

---

## 📊 Vista General (Gantt Chart)

```mermaid
gantt
    title Roadmap LANCEA - Semestre 1
    dateFormat  X
    axisFormat Sem %s
    
    section Fase 1: Diseño
    Análisis y Re-Ingeniería (IMU vs Ultrasonido)   :done,    des1, 0, 2w
    Adquisición de Componentes                      :done,    des2, 1w, 1w
    Diseño Electrónico (Pinout/Diagramas)           :active,  des3, 2w, 1w
    Diseño Conceptual 3D (Sled)                     :active,  des4, 2w, 1w
    
    section Fase 2: Firmware
    Pruebas Unitarias (Hola Mundo Hardware)         :active,  dev1, 2.5w, 1.5w
    Desarrollo Driver BNO055 + Algoritmo IMU        :         dev2, 4w, 3w
    Integración Pantalla OLED y UI                  :         dev3, 6w, 2w
    Sistema de Archivos (SD Logging)                :         dev4, 8w, 2w
    
    section Fase 3: Integración
    Ensamblaje PCB y Chasis 3D                      :         int1, 10w, 2w
    Pruebas de Campo (Lanzamientos)                 :         int2, 12w, 2w
    
    section Fase 4: Cierre
    Documentación Final y Sustentación              :         doc1, 14w, 2w
