# 📅 Cronograma de Ejecución - Proyecto LANCEA



Este documento detalla el plan de trabajo semestral, el seguimiento de hitos y el estado actual del desarrollo del sistema.



**Estado Actual:** 🟡 Semana 3 (En Ejecución)

**Fase:** Diseño Detallado y Pruebas Unitarias

**Semestre:** 2026-I



---



## 📊 Vista General (Gantt Chart)



> La línea roja vertical indica la fecha actual.



```mermaid

gantt

    title Cronograma LANCEA - Semestre 2026-I

    dateFormat  YYYY-MM-DD

    axisFormat  Sem %W

    todayMarker on



    section Fase 1: Diseño y Gestión

    Análisis y Re-Ingeniería (IMU vs Ultrasonido)   :done,    des1, 2026-02-03, 12d

    Compra de Componentes                           :done,    des2, 2026-02-10, 5d

    Diseño Pinout y Diagramas                       :active,  des3, 2026-02-17, 5d

    Diseño Conceptual 3D (Sled)                     :active,  des4, 2026-02-17, 5d



    section Fase 2: Firmware

    Pruebas Unitarias (Hola Mundo Hardware)         :active,  dev1, 2026-02-20, 7d

    Desarrollo Driver BNO055 + Algoritmo IMU        :         dev2, after dev1, 14d

    Integración Pantalla OLED y UI                  :         dev3, after dev2, 7d

    Sistema de Archivos (SD Logging)                :         dev4, after dev3, 10d



    section Fase 3: Integración

    Ensamblaje PCB y Chasis 3D                      :         int1, after dev4, 7d

    Pruebas de Campo (Lanzamientos)                 :         int2, after int1, 14d



    section Fase 4: Cierre

    Documentación Final                             :         doc1, after int2, 14d

    Sustentación Final                              :crit,    milestone, after doc1, 0d

