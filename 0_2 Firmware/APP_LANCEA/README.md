# LANCEA — Guía de Instalación y Uso
## Sistema de Telemetría Inteligente para Jabalina
LANCEA es una herramienta diseñada para convertir cada lanzamiento de jabalina en datos reales que ayudan a mejorar la técnica. En esta guía, aprenderás paso a paso cómo preparar el sensor (el "cerebro" que va en la jabalina) y cómo instalar la aplicación en tu computadora. Con este sistema, podrás ver la potencia y el ángulo de cada tiro en tiempo real, ya sea usando un cable o conectándote sin cables por WiFi desde tu celular en la pista de entrenamiento. Sigue estos pasos para transformar el esfuerzo físico en información inteligente para ganar distancia.

---

## ¿Qué necesitas?

### Hardware
| Componente | Descripción |
|---|---|
| XIAO ESP32-C3 | Microcontrolador principal |
| BNO055 | Sensor IMU (acelerómetro + giroscopio) |
| Batería LiPo 3.7V | Para uso en campo sin PC |
| Cable USB-C | Para programar y conectar a la App |

### Conexiones del hardware
```
BNO055  →  XIAO ESP32-C3
VCC     →  3.3V
GND     →  GND
SDA     →  D4 (GPIO 6)
SCL     →  D5 (GPIO 7)
```

---

## PARTE 1 — Configurar el XIAO ESP32-C3

### Paso 1 — Instalar Arduino IDE
1. Descarga Arduino IDE desde https://www.arduino.cc/en/software
2. Instálalo normalmente

### Paso 2 — Agregar soporte para ESP32
1. Abre Arduino IDE
2. Ve a **Archivo → Preferencias**
3. En "URLs adicionales para el gestor de placas" pega:
   ```
   [https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json](https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json)
   ```
4. Ve a **Herramientas → Placa → Gestor de placas**
5. Busca `esp32` e instala **ESP32 by Espressif Systems**

### Paso 3 — Instalar librerías del sensor
Ve a **Herramientas → Administrar Librerías** e instala:
- `Adafruit BNO055`
- `Adafruit Unified Sensor`

### Paso 4 — Seleccionar la placa
1. **Herramientas → Placa → esp32 → XIAO_ESP32C3**
2. **Herramientas → Puerto** → selecciona el COM que aparece al conectar el XIAO

### Paso 5 — Elegir el firmware correcto

| Archivo | Cuándo usarlo |
|---|---|
| `LANCEA_WiFi.ino` | **Recomendado** — campo con batería + WiFi |
| `LANCEA_NoSD.ino` | Solo cable USB + App en tiempo real |

### Paso 6 — Subir el firmware
1. Abre el archivo `.ino` en Arduino IDE
2. Haz clic en el botón **→ Subir**
3. Espera a que diga "Subida completada"
4. Abre el **Monitor Serial** a **115200 baud**
5. Deberías ver:
   ```
   LANCEA  WiFi  v7.0  —  XIAO ESP32-C3
   [OK]   BNO055 listo.
   [WiFi] SSID: LANCEA_AP
   [WiFi] IP  : 192.168.4.1
   >>> Listo. Esperando lanzamiento...
   ```

---

## PARTE 2 — Instalar la App LANCEA en el PC

### Paso 1 — Instalar Python
1. Descarga Python 3.10 o superior desde https://www.python.org/downloads/
2. Durante la instalación marca la casilla **"Add Python to PATH"**
3. Verifica abriendo CMD y escribiendo: `python --version`

### Paso 2 — Instalar dependencias
Abre CMD (Windows) o Terminal (Mac/Linux) y ejecuta:
```
pip install customtkinter pyserial pandas numpy matplotlib
```

### Paso 3 — Ejecutar la App
1. Descarga el archivo `lancea_app.py`
2. Colócalo en una carpeta de tu elección (ej. `C:\LANCEA\`)
3. En CMD navega a esa carpeta:
   ```
   cd C:\LANCEA
   python lancea_app.py
   ```
4. La App se abrirá automáticamente

> **Atajo (Windows):** crea un archivo `iniciar.bat` en la misma carpeta con:
> ```
> python lancea_app.py
> pause
> ```
> Doble clic para abrir la App sin tocar el CMD.

---

## PARTE 3 — Uso en modo USB (tiempo real)

### Conexión
1. Conecta el XIAO al PC con el cable USB
2. Abre la App LANCEA
3. En el módulo **TELEMETRÍA EN VIVO**:
   - Selecciona el puerto COM en el desplegable
   - Haz clic en **CONECTAR ESP32**
   - El LED del XIAO parpadea lento = listo

### Primer lanzamiento
1. Selecciona el atleta en el menú del sidebar
2. Realiza el lanzamiento
3. Los KPIs aparecen en tiempo real en la pantalla
4. El Coach Virtual da feedback inmediato
5. El lanzamiento queda guardado automáticamente en:
   ```
   LANCEA_DATA/atletas/<nombre>/<fecha>/1_datos_crudos/
   ```

### Obtener historial
- Botón **DUMP** → descarga todos los lanzamientos de la sesión
- Módulo **ANALIZADOR** → abre el CSV guardado para ver gráficas

---

## PARTE 4 — Uso en campo (WiFi, sin PC)

### Preparación
1. Conecta la batería LiPo al pin BAT del XIAO
2. El XIAO enciende y crea la red **LANCEA_AP**
3. El LED parpadea lento = sistema listo

### Durante el entrenamiento
- Realiza los lanzamientos normalmente
- El XIAO detecta cada impulso y guarda en memoria
- LED fijo = detectando impulso
- 3 destellos rápidos = lanzamiento registrado

### Ver datos desde el celular
1. Ve a WiFi en el celular
2. Conecta a la red: **LANCEA_AP** (clave: `lancea123`)
3. Abre el navegador y ve a: **192.168.4.1**
4. Verás la tabla con todos los lanzamientos

### Gestionar atletas desde el celular
1. Ve a **192.168.4.1/atletas**
2. Escribe el nombre y toca **+ Registrar**
3. Toca **Seleccionar** para activar un atleta
4. Cada lanzamiento queda vinculado al atleta activo

### Descargar CSV desde el celular
- Toca **↓ Descargar CSV** en la página principal
- El archivo se guarda en el celular
- Compártelo por WhatsApp, Drive o cable al PC

### Ver datos desde el PC (con WiFi)
1. Conecta el PC a la red **LANCEA_AP**
2. Abre la App LANCEA
3. Ve al módulo **WiFi · PANEL & ATLETAS**
4. Escribe la IP `192.168.4.1` y toca **Conectar**
5. Verás los atletas, sus lanzamientos y badges de rendimiento
6. Toca **Importar CSV** para traer los datos al analizador

---

## PARTE 5 — Archivos y estructura de datos

```
LANCEA_DATA/
├── config.json                    ← configuración de la App
├── sd_imports/                    ← volcados desde WiFi o SD
└── atletas/
    └── Juan Perez/
        └── 2025-03-22/
            ├── 1_datos_crudos/    ← sesion_HHMMSS.csv + .log
            ├── 2_graficas/        ← grafica_HHMMSS.png
            └── 3_analisis/        ← estadisticas_HHMMSS.csv
```

El reporte gráfico se genera **automáticamente** después de cada lanzamiento.
Para abrirlo: módulo **ANALIZADOR → 📂 ABRIR REPORTES**.

---

## PARTE 6 — Calibración de umbrales

Con el DEBUG_MODE activado en el firmware, abre el Monitor Serial
y observa la columna `Jerk` mientras mueves el sensor:

| Situación | Jerk esperado |
|---|---|
| Sensor en reposo | < 5 |
| Caminar normal | 5 – 20 |
| Sacudida fuerte de escritorio | 20 – 40 |
| Lanzamiento real de jabalina | 50 – 150 |

Ajusta `JERK_THRESHOLD` entre el valor en reposo y el de lanzamiento.
Cuando esté calibrado, cambia `DEBUG_MODE` de `1` a `0` y vuelve a subir.

---

## Solución de problemas comunes

| Problema | Solución |
|---|---|
| BNO055 no detectado | Verifica SDA=D4, SCL=D5. Prueba dirección 0x29 |
| Puerto COM no aparece | Instala driver CH340: https://www.wch-ic.com/downloads/CH341SER_ZIP.html |
| App no abre | Verifica que Python está en PATH. Reinstala con `pip install --upgrade customtkinter` |
| Página 192.168.4.1 no carga | El celular dice "sin internet" — eso es normal, igual debe cargar |
| Datos se pierden al quitar USB | El XIAO se reinicia por señal DTR. Solución: condensador 10µF entre RST y GND |
| Lanzamientos no se detectan | Baja `JERK_THRESHOLD` y activa `DEBUG_MODE 1` para calibrar |

---

## Resumen rápido de comandos

```bash
# Instalar dependencias (una sola vez)
pip install customtkinter pyserial pandas numpy matplotlib

# Abrir la App
python lancea_app.py
```

```
# Comandos seriales (en el Monitor Arduino o desde la App)
DUMP    → exporta historial de lanzamientos en CSV
RESET   → borra historial y reinicia contador
```

---

*LANCEA © 2025 — Sistema de Telemetría Inteligente para Jabalina*
