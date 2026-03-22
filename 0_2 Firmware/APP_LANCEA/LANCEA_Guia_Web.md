# LANCEA — Guía del Servidor Web WiFi
## Página 192.168.4.1 — Manual de uso desde celular o PC

---

## Antes de empezar

El XIAO ESP32-C3 crea su propia red WiFi al encenderse.
No necesitas internet. La página la sirve el propio dispositivo.

### Conectarse a la red

**Desde el celular:**
1. Abre **Configuración → WiFi**
2. Busca la red **LANCEA_AP**
3. Contraseña: **lancea123**
4. El celular puede mostrar "Sin internet" — eso es normal, la página carga igual
5. Abre el navegador y escribe: **192.168.4.1**

**Desde el PC:**
1. Haz clic en el icono WiFi de la barra de tareas
2. Conecta a **LANCEA_AP** (clave: lancea123)
3. Abre cualquier navegador y escribe: **192.168.4.1**

> El navegador recomendado es Chrome o Safari.
> Si la página no carga a la primera, recarga con F5.

---

## Mapa del sitio

```
192.168.4.1/            Panel principal — lanzamientos del atleta activo
192.168.4.1/atletas     Gestión de atletas — registrar / activar / borrar
192.168.4.1/csv         Descargar CSV del atleta activo
192.168.4.1/csv?a=Todos Descargar CSV de TODOS los atletas juntos
192.168.4.1/status      JSON con estado del dispositivo (para diagnóstico)
192.168.4.1/reset       Borrar lanzamientos del atleta activo
192.168.4.1/resetall    Borrar absolutamente todo
```

La barra de navegación en la parte superior de cada página
tiene dos enlaces rápidos: **Panel** y **Atletas**.

---

## Página 1 — Panel Principal (`192.168.4.1/`)

Es la página de inicio. Muestra el rendimiento del atleta activo.

### Barra de estado superior
```
🟢 EN ESPERA  |  Atleta: Juan Perez  |  3 lanzamiento(s)
```
| Icono | Significado |
|---|---|
| 🟢 EN ESPERA | Listo para detectar el siguiente lanzamiento |
| 🔴 INTEGRANDO | Impulso detectado, calculando velocidad |
| 🟠 PAUSA | Lanzamiento registrado, esperando 3 segundos |

### Badges de rendimiento
Aparecen automáticamente cuando hay al menos 1 lanzamiento:

| Badge | Qué muestra |
|---|---|
| **Vel max m/s** | Velocidad de salida más alta de la sesión |
| **Ang prom** | Promedio de ángulos de todos los lanzamientos |
| **Dist max m** | Distancia estimada más larga |
| **Energia max J** | Energía cinética más alta |

### Tabla de lanzamientos
Muestra solo los lanzamientos del atleta activo.

| Columna | Descripción |
|---|---|
| # | Número de lanzamiento en la sesión |
| Vel (m/s) | Velocidad de salida calculada |
| Ang | Ángulo de liberación en grados |
| Dist (m) | Distancia estimada (modelo proyectil) |
| Acel | Aceleración máxima durante el impulso |
| t (s) | Duración del impulso |
| E (J) | Energía cinética del lanzamiento |
| P (W) | Potencia media aplicada |
| Ang? | Calificación del ángulo |

**Calificación del ángulo:**
| Color | Etiqueta | Rango |
|---|---|---|
| 🟢 Verde | Optimo | 32° – 39° |
| 🟡 Amarillo | Bajo | 28° – 31° |
| 🟡 Amarillo | Alto | 40° – 44° |
| 🔴 Rojo | Malo | Fuera de rango |

### Botones
| Botón | Acción |
|---|---|
| **↓ CSV [nombre atleta]** | Descarga el CSV solo con los lanzamientos del atleta activo |
| **↓ CSV Todos** | Descarga un CSV con todos los atletas y todos los lanzamientos |
| **✕ Reset atleta** | Borra los lanzamientos del atleta activo (pide confirmación) |
| **▷ Gestionar atletas** | Va a la página de gestión de atletas |

---

## Página 2 — Gestión de Atletas (`192.168.4.1/atletas`)

Desde aquí se controla quién está lanzando.

### Lista de atletas registrados
Muestra una tabla con todos los atletas en memoria:

```
Nombre          Lanzamientos   Acción
──────────────────────────────────────────
► Juan Perez    3              [Activo]
  Maria Lopez   0              [Seleccionar]
  Pedro Garcia  5              [Seleccionar] [✕]
  Invitado      0              [Seleccionar]
```

- El símbolo **►** y el color azul indican el atleta activo
- **[Seleccionar]** → cambia el atleta activo inmediatamente
- **[✕]** → borra el atleta de la lista (sus lanzamientos quedan guardados bajo "Invitado")
- El atleta **Invitado** no se puede borrar

> **Importante:** al seleccionar un atleta, los siguientes lanzamientos
> quedan registrados a su nombre. Los lanzamientos anteriores no cambian.

### Registrar nuevo atleta
1. Escribe el nombre en el campo de texto
2. Toca o haz clic en **+ Registrar**
3. El atleta queda registrado y se activa automáticamente
4. Límite: 10 atletas simultáneos en memoria

> Los nombres se guardan en RAM. Si el dispositivo se reinicia,
> los atletas se pierden. Descarga el CSV antes de apagar.

---

## Descargar CSV

### Desde la página principal
- Toca **↓ CSV [nombre]** para el CSV del atleta activo
- Toca **↓ CSV Todos** para exportar toda la sesión

### Formato del archivo CSV
```
# LANCEA - Sesion de Lanzamientos
# Atleta: Juan Perez
num,Atleta,Velocidad,Angulo,Distancia,maxAccel,impulseTime,Energia,Potencia
1,Juan Perez,14.20,36.5,21.30,32.10,0.410,81.12,197.85
2,Juan Perez,15.05,37.1,23.40,35.20,0.390,91.20,233.85
```

Las líneas que empiezan con `#` son comentarios informativos.
La primera fila de datos es la cabecera de columnas.

### Cómo llevar el CSV al PC
| Método | Pasos |
|---|---|
| **WhatsApp** | Descarga el archivo → abre WhatsApp → envíatelo a ti mismo |
| **Google Drive** | Descarga → abre Drive → sube el archivo |
| **Cable USB** | Conecta el celular al PC → copia desde la carpeta Descargas |
| **Email** | Descarga → adjunta en un correo y envíatelo |

Una vez en el PC, abre la App LANCEA → módulo **ANALIZADOR**
→ **📂 ABRIR ARCHIVO** → selecciona el CSV → análisis automático.

---

## Página de Estado (`192.168.4.1/status`)

Devuelve un JSON útil para diagnóstico:

```json
{
  "throws": 3,
  "atleta_activo": "Juan Perez",
  "num_atletas": 2,
  "estado": "IDLE",
  "uptime_s": 1842
}
```

| Campo | Descripción |
|---|---|
| throws | Total de lanzamientos en memoria |
| atleta_activo | Nombre del atleta activo actualmente |
| num_atletas | Cuántos atletas están registrados |
| estado | IDLE / IMPULSO / PAUSA |
| uptime_s | Segundos desde que encendió el dispositivo |

---

## Flujo completo de un día de entrenamiento

```
ANTES DE EMPEZAR
  1. Enciende el XIAO con batería
  2. Conéctate a LANCEA_AP
  3. Ve a 192.168.4.1/atletas
  4. Registra a cada atleta que va a lanzar hoy
  5. Selecciona el primer atleta

DURANTE EL ENTRENAMIENTO
  6. El atleta lanza → el dispositivo detecta y guarda automáticamente
  7. Refresca la página para ver el nuevo lanzamiento en la tabla
  8. Cuando cambia el atleta → ve a /atletas → toca [Seleccionar]
  9. Los siguientes lanzamientos quedan bajo el nuevo nombre

AL TERMINAR
  10. Ve a 192.168.4.1
  11. Toca "↓ CSV Todos" → descarga el archivo con toda la sesión
  12. Comparte el CSV al PC (WhatsApp, Drive, cable)
  13. Abre la App LANCEA en el PC → carga el CSV → análisis completo
```

---

## Preguntas frecuentes

**¿Cuántos lanzamientos guarda el dispositivo?**
Hasta 100 lanzamientos en total entre todos los atletas. El pie de página
muestra cuántos slots quedan disponibles.

**¿Qué pasa si se llena la memoria?**
Los nuevos lanzamientos no se guardan. Descarga el CSV y usa
`192.168.4.1/reset` o `192.168.4.1/resetall` para liberar espacio.

**¿Tengo que recargar la página manualmente?**
Sí. La página no se actualiza sola. Recarga con el botón del navegador
o arrastra hacia abajo en el celular después de cada lanzamiento.

**¿Puedo tener el celular y el PC conectados al mismo tiempo?**
Sí. Varios dispositivos pueden conectarse a LANCEA_AP simultáneamente
y ver la página al mismo tiempo.

**¿Se pierden los datos si apago el XIAO?**
Sí — todo está en RAM. Siempre descarga el CSV antes de apagar.

**El botón Reset no pide contraseña, ¿es peligroso?**
El botón **✕ Reset atleta** sí pide confirmación en el navegador.
El botón `192.168.4.1/resetall` borra todo sin confirmación —
úsalo con cuidado o solo cuando estés seguro de haber descargado el CSV.

---

*LANCEA © 2025 — Servidor Web v7.0 — XIAO ESP32-C3*
