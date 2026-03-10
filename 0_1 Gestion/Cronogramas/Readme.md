gantt
    title Cronograma LANCEA - Semestre 2026-I
    dateFormat  YYYY-MM-DD
    axisFormat  Sem %W
    todayMarker on

    section Fase 1: Diseño y Gestión
    Análisis y Re-Ingeniería      :done,    des1, 2026-02-02, 14d
    Compra de Componentes         :done,    des2, 2026-02-16, 7d
    Diseño Pinout y Diagramas     :done,    des3, 2026-02-23, 7d
    Entrega Portafolio 1 (Sem 5)  :milestone, done, m1, 2026-03-02, 0d

    section Fase 2: Firmware & Hardware (Actual)
    Pruebas Unitarias de Hardware :done,    dev1, 2026-03-02, 14d
    Desarrollo Firmware ESP32     :active,  dev2, 2026-03-16, 14d
    Fabricación PCB Definitiva    :active,  dev3, 2026-03-16, 14d
    Eval. Proyecto/Portafolio (Sem 9) :milestone, m2, 2026-03-30, 0d

    section Fase 3: Integración PMV
    Ensamblaje PCB y Chasis 3D    :         int1, 2026-03-30, 14d
    Pruebas de Usabilidad         :         int2, 2026-04-13, 14d
    Cierre de Desarrollo (Sem 13) :milestone, m3, 2026-04-27, 0d

    section Fase 4: Cierre y Sustentación
    Presentación al Cliente (Sem 14) :crit, milestone, m4, 2026-05-04, 0d
    Sustentación Final (Sem 15)      :crit, milestone, m5, 2026-05-11, 0d
    Ajustes y Modificaciones         :         doc1, 2026-05-04, 14d
    Cierre Definitivo (Sem 16)       :milestone, m6, 2026-05-18, 0d
