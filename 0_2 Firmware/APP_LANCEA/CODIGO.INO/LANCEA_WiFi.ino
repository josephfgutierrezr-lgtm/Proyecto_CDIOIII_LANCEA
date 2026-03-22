// ================================================================
//  LANCEA_WiFi.ino  —  XIAO ESP32-C3  v7.0
//  Sistema de atletas desde la pagina web
//
//  NOVEDADES v7.0:
//  · Hasta 10 atletas registrados en RAM
//  · Selector de atleta activo desde celular/PC
//  · Cada lanzamiento queda vinculado al atleta
//  · Pagina /atletas  → gestionar atletas (agregar/seleccionar/borrar)
//  · CSV y tabla filtrados por atleta activo
//  · /csv?atleta=Todos  → exporta todos los atletas juntos
//
//  PAGINAS WEB:
//    192.168.4.1/          → panel principal (atleta activo)
//    192.168.4.1/atletas   → gestionar atletas
//    192.168.4.1/csv       → CSV del atleta activo
//    192.168.4.1/csv?a=Todos → CSV de todos
//    192.168.4.1/status    → JSON estado
//    192.168.4.1/reset     → borra lanzamientos del atleta activo
//    192.168.4.1/resetall  → borra todo
// ================================================================

#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>
#include <WiFi.h>
#include <WebServer.h>

// ================================================================
//  CONFIGURACION WiFi
// ================================================================
const char*     AP_SSID = "LANCEA_AP";
const char*     AP_PASS = "lancea123";
const IPAddress AP_IP(192, 168, 4, 1);

// ================================================================
//  PINES  XIAO ESP32-C3
// ================================================================
#define I2C_SDA  6
#define I2C_SCL  7
#define LED_PIN 10

// ================================================================
//  PARAMETROS FISICOS
// ================================================================
const double g            = 9.81;
const double JAVELIN_MASS = 0.8;

// ================================================================
//  PARAMETROS DEL ALGORITMO
// ================================================================
const double ALPHA              = 0.30;
const double JERK_THRESHOLD     = 50.0;
const double FREEFALL_THRESHOLD = 0.8;
const double ARMING_ACCEL       = 15.0;
const unsigned long TIMEOUT_MS  = 2000;
const unsigned long PAUSE_MS    = 3000;

// ================================================================
//  TIMING
// ================================================================
Adafruit_BNO055     bno          = Adafruit_BNO055(55, 0x28);
const unsigned long INTERVALO_US = 10000UL;
const double        DT           = 0.01;
unsigned long       lastTime_us  = 0;

// ================================================================
//  MAQUINA DE ESTADOS
// ================================================================
enum Estado { IDLE, IMPULSO, PAUSA };
Estado        estadoActual = IDLE;
unsigned long tEstado      = 0;

// ================================================================
//  LED NO BLOQUEANTE
// ================================================================
struct LedFSM {
  int total=0, done=0, ms=120;
  bool on=false, running=false;
  unsigned long tLed=0;

  void blink(int n, int interval=120) {
    total=n*2; done=0; on=false; ms=interval;
    running=true; tLed=millis();
    digitalWrite(LED_PIN, HIGH);
  }
  void update() {
    if (!running) return;
    if (millis()-tLed < (unsigned long)ms) return;
    tLed=millis(); on=!on;
    digitalWrite(LED_PIN, on ? LOW : HIGH);
    if (++done >= total) { running=false; digitalWrite(LED_PIN, HIGH); }
  }
} led;

// ================================================================
//  SISTEMA DE ATLETAS
// ================================================================
#define MAX_ATLETAS  10
#define MAX_NAME_LEN 24

struct Atleta {
  char   nombre[MAX_NAME_LEN];
  bool   activo;
};

Atleta atletas[MAX_ATLETAS];
int    numAtletas    = 0;
int    atletaActivo  = -1;   // -1 = sin seleccion

// Agrega atleta, devuelve indice o -1 si esta lleno/duplicado
int agregarAtleta(const String& nombre) {
  String n = nombre; n.trim();
  if (n.length() == 0 || n.length() >= MAX_NAME_LEN) return -1;
  for (int i=0; i<numAtletas; i++)
    if (String(atletas[i].nombre) == n) return i;   // ya existe
  if (numAtletas >= MAX_ATLETAS) return -1;
  n.toCharArray(atletas[numAtletas].nombre, MAX_NAME_LEN);
  atletas[numAtletas].activo = false;
  return numAtletas++;
}

void seleccionarAtleta(int idx) {
  if (idx < 0 || idx >= numAtletas) return;
  atletaActivo = idx;
}

String nombreActivo() {
  if (atletaActivo < 0 || atletaActivo >= numAtletas)
    return "Sin atleta";
  return String(atletas[atletaActivo].nombre);
}

// ================================================================
//  HISTORIAL RAM — con referencia al atleta
// ================================================================
#define MAX_THROWS 100

struct ThrowRecord {
  uint8_t num;
  float   velFinal, maxAccel, angle, impulseTime, distance, energy, power;
  int8_t  atletaIdx;   // indice en atletas[], -1 si no habia atleta
};

ThrowRecord throwLog[MAX_THROWS];
int         throwLogCount = 0;
int         throwCount    = 0;   // contador global de la sesion

// ================================================================
//  SERVIDOR WEB
// ================================================================
WebServer server(80);

// ================================================================
//  VARIABLES DE VUELO
// ================================================================
double        v_x=0, v_y=0, v_z=0;
double        ax_f=0, ay_f=0, az_f=0;
double        prev_aMag=0, maxAccel=0, launchAngle=0;
unsigned long startImpulse=0;

// ================================================================
//  SERIAL SEGURO
// ================================================================
void safePrint(const String& s) {
  if (Serial && Serial.availableForWrite()>10) Serial.print(s);
}
void safePrintln(const String& s) {
  if (Serial && Serial.availableForWrite()>10) Serial.println(s);
}

// ================================================================
//  PROTOTIPOS
// ================================================================
void   initWiFi();
void   registerRoutes();
void   handleRoot();
void   handleAtletas();
void   handleSetAtleta();
void   handleAddAtleta();
void   handleDelAtleta();
void   handleCSV();
void   handleStatus();
void   handleResetAtleta();
void   handleResetAll();
void   handleCommands();
void   handleDump();
void   handleReset();
void   publishThrow(double v,double a,double t,double d,double e,double p);
void   resetVariables();
String buildCSV(int filterAtleta);
String htmlHeader(const String& title);
String htmlFooter();

// ================================================================
//  SETUP
// ================================================================
void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, HIGH);
  delay(3000);

  Wire.begin(I2C_SDA, I2C_SCL);

  safePrintln("================================================");
  safePrintln("  LANCEA  WiFi  v7.0  —  XIAO ESP32-C3");
  safePrintln("================================================");

  // Atleta por defecto
  agregarAtleta("Invitado");
  seleccionarAtleta(0);

  if (!bno.begin()) {
    safePrintln("[ERROR] BNO055 no detectado.");
    while(1) delay(1000);
  }
  bno.setExtCrystalUse(true);
  safePrintln("[OK]   BNO055 listo.");

  initWiFi();
  registerRoutes();
  server.begin();

  safePrintln("[WEB]  http://192.168.4.1");
  safePrintln("[WEB]  http://192.168.4.1/atletas");
  safePrintln(">>> Listo. Atleta: " + nombreActivo());
  safePrintln("------------------------------------------------");

  led.blink(3, 200);
}

void initWiFi() {
  WiFi.mode(WIFI_AP);
  WiFi.softAPConfig(AP_IP, AP_IP, IPAddress(255,255,255,0));
  WiFi.softAP(AP_SSID, AP_PASS);
  safePrintln("[WiFi] SSID: " + String(AP_SSID));
  safePrintln("[WiFi] IP  : " + WiFi.softAPIP().toString());
}

void registerRoutes() {
  server.on("/",            HTTP_GET,  handleRoot);
  server.on("/atletas",     HTTP_GET,  handleAtletas);
  server.on("/set_atleta",  HTTP_GET,  handleSetAtleta);
  server.on("/add_atleta",  HTTP_POST, handleAddAtleta);
  server.on("/del_atleta",  HTTP_GET,  handleDelAtleta);
  server.on("/csv",         HTTP_GET,  handleCSV);
  server.on("/status",      HTTP_GET,  handleStatus);
  server.on("/reset",       HTTP_GET,  handleResetAtleta);
  server.on("/resetall",    HTTP_GET,  handleResetAll);
  server.onNotFound([](){
    server.sendHeader("Location","/");
    server.send(302,"text/plain","");
  });
}

// ================================================================
//  LOOP PRINCIPAL — 100% no bloqueante
// ================================================================
void loop() {
  server.handleClient();
  handleCommands();
  led.update();

  switch (estadoActual) {
    case IDLE: {
      static unsigned long tB=0; static bool bS=false;
      if (!led.running && millis()-tB>=1200) {
        tB=millis(); bS=!bS;
        digitalWrite(LED_PIN, bS ? LOW : HIGH);
      }
      break;
    }
    case PAUSA:
      if (millis()-tEstado >= PAUSE_MS) {
        resetVariables();
        estadoActual = IDLE;
      }
      break;
    default: break;
  }

  unsigned long now_us = micros();
  if (now_us - lastTime_us < INTERVALO_US) return;
  lastTime_us = now_us;

  if (estadoActual == PAUSA) return;

  sensors_event_t ev;
  bno.getEvent(&ev, Adafruit_BNO055::VECTOR_LINEARACCEL);
  double ax=ev.acceleration.x, ay=ev.acceleration.y, az=ev.acceleration.z;

  ax_f = ALPHA*ax + (1.0-ALPHA)*ax_f;
  ay_f = ALPHA*ay + (1.0-ALPHA)*ay_f;
  az_f = ALPHA*az + (1.0-ALPHA)*az_f;

  double aMag = sqrt(ax_f*ax_f + ay_f*ay_f + az_f*az_f);
  double jerk = (aMag - prev_aMag) / DT;
  prev_aMag = aMag;

  if (estadoActual==IDLE && jerk>JERK_THRESHOLD) {
    estadoActual = IMPULSO;
    startImpulse = millis();
    digitalWrite(LED_PIN, LOW);

    imu::Quaternion quat = bno.getQuat();
    imu::Vector<3>  euler = quat.toEuler();
    launchAngle = euler.y() * 180.0 / PI;

    safePrintln("IMPULSO_START");
    safePrintln("Atleta: " + nombreActivo());
  }

  if (estadoActual==IMPULSO) {
    v_x += ax_f*DT; v_y += ay_f*DT; v_z += az_f*DT;
    if (aMag > maxAccel) maxAccel = aMag;

    if (aMag < FREEFALL_THRESHOLD && maxAccel > ARMING_ACCEL) {
      double impulseTime = (millis()-startImpulse)/1000.0;
      double velFinal    = sqrt(v_x*v_x + v_y*v_y + v_z*v_z);
      double angleRad    = launchAngle * PI / 180.0;
      double distance    = (velFinal*velFinal*sin(2.0*angleRad)) / g;
      double energy      = 0.5 * JAVELIN_MASS * velFinal * velFinal;
      double power       = (impulseTime>0) ? energy/impulseTime : 0.0;

      throwCount++;

      if (throwLogCount < MAX_THROWS) {
        throwLog[throwLogCount++] = {
          (uint8_t)throwCount,
          (float)velFinal, (float)maxAccel, (float)launchAngle,
          (float)impulseTime, (float)distance,
          (float)energy, (float)power,
          (int8_t)atletaActivo
        };
      }

      publishThrow(velFinal, launchAngle, impulseTime, distance, energy, power);
      led.blink(3);
      estadoActual = PAUSA;
      tEstado = millis();
      return;
    }

    if ((millis()-startImpulse) > TIMEOUT_MS) {
      safePrintln("[!] Timeout.");
      resetVariables();
      estadoActual = IDLE;
    }
  }
}

// ================================================================
//  HELPERS HTML
// ================================================================
String htmlHeader(const String& title) {
  String h = "<!DOCTYPE html><html lang='es'><head><meta charset='UTF-8'>";
  h += "<meta name='viewport' content='width=device-width,initial-scale=1'>";
  h += "<title>LANCEA - " + title + "</title><style>";
  h += "body{background:#03060A;color:#E8F4FD;font-family:monospace;margin:0;padding:14px}";
  h += "h1{color:#00C8FF;font-size:1.3em;margin-bottom:2px}";
  h += "h2{color:#6B8BA4;font-size:1em;margin:16px 0 8px}";
  h += ".sub{color:#334B62;font-size:.8em;margin-bottom:12px}";
  h += ".badge{display:inline-block;background:#0F1C2E;border:1px solid #1A3050;";
  h += "border-radius:6px;padding:6px 14px;margin:3px;text-align:center}";
  h += ".badge span{display:block;font-size:1.5em;font-weight:bold}";
  h += ".v{color:#00C8FF}.a{color:#F0A500}.d{color:#00FF88}.e{color:#A855F7}.p{color:#EC4899}";
  h += "table{width:100%;border-collapse:collapse;font-size:.82em;margin-top:8px}";
  h += "th{background:#0B1520;color:#6B8BA4;padding:7px 5px;text-align:center;border-bottom:1px solid #1A3050}";
  h += "td{padding:6px 5px;text-align:center;border-bottom:1px solid #0B1520}";
  h += "tr:hover td{background:#0B1520}";
  h += ".btn{display:inline-block;margin:6px 3px;padding:8px 18px;background:#00C8FF;";
  h += "color:#000;border-radius:6px;font-family:monospace;font-weight:bold;text-decoration:none;border:none;cursor:pointer}";
  h += ".btn-green{background:#00FF88;color:#000}";
  h += ".btn-red{background:#FF3B5C;color:#fff}";
  h += ".btn-gray{background:#0F1C2E;color:#E8F4FD;border:1px solid #1A3050}";
  h += ".btn-active{background:#F0A500;color:#000}";
  h += ".ok{color:#00FF88}.warn{color:#F0A500}.bad{color:#FF3B5C}";
  h += "input[type=text]{background:#0F1C2E;color:#E8F4FD;border:1px solid #1A3050;";
  h += "border-radius:6px;padding:8px 12px;font-family:monospace;font-size:1em;width:200px}";
  h += ".nav{margin-bottom:16px}";
  h += ".nav a{color:#6B8BA4;text-decoration:none;margin-right:16px;font-size:.85em}";
  h += ".nav a:hover{color:#00C8FF}";
  h += ".atleta-activo{color:#00C8FF;font-weight:bold}";
  h += "</style></head><body>";
  h += "<div class='nav'><a href='/'>Panel</a><a href='/atletas'>Atletas</a></div>";
  return h;
}

String htmlFooter() {
  String f = "<br><div style='color:#334B62;font-size:.75em;margin-top:20px'>";
  f += "LANCEA v7.0 | RAM: " + String(MAX_THROWS-throwLogCount) + " slots libres";
  f += " | Atleta: <span class='atleta-activo'>" + nombreActivo() + "</span>";
  f += "</div></body></html>";
  return f;
}

// ================================================================
//  PAGINA PRINCIPAL  /
// ================================================================
void handleRoot() {
  server.setContentLength(CONTENT_LENGTH_UNKNOWN);
  server.send(200, "text/html; charset=utf-8", "");
  server.sendContent(htmlHeader("Panel"));

  // Estado + atleta activo
  String s = "<h1>&#9651; LANCEA</h1>";
  s += "<div class='sub'>";
  s += estadoActual==IMPULSO ? "&#128308; INTEGRANDO" :
       estadoActual==PAUSA   ? "&#128992; PAUSA" :
                               "&#128994; EN ESPERA";
  s += " &nbsp;|&nbsp; Atleta: <span class='atleta-activo'>" + nombreActivo() + "</span>";

  // Contar lanzamientos del atleta activo
  int cuentaActivo = 0;
  for (int i=0;i<throwLogCount;i++)
    if (throwLog[i].atletaIdx == atletaActivo) cuentaActivo++;
  s += " &nbsp;|&nbsp; " + String(cuentaActivo) + " lanzamiento(s)</div>";
  server.sendContent(s);

  // Badges del atleta activo
  float bestV=0,bestD=0,bestE=0,sumA=0; int cnt=0;
  for (int i=0;i<throwLogCount;i++) {
    if (throwLog[i].atletaIdx != atletaActivo) continue;
    if(throwLog[i].velFinal>bestV) bestV=throwLog[i].velFinal;
    if(throwLog[i].distance>bestD) bestD=throwLog[i].distance;
    if(throwLog[i].energy  >bestE) bestE=throwLog[i].energy;
    sumA+=throwLog[i].angle; cnt++;
  }
  if (cnt > 0) {
    float avgA=sumA/cnt;
    s  = "<div class='badge'><span class='v'>"+String(bestV,2)+"</span>Vel max m/s</div>";
    s += "<div class='badge'><span class='a'>"+String(avgA,1)+"</span>Ang prom</div>";
    s += "<div class='badge'><span class='d'>"+String(bestD,2)+"</span>Dist max m</div>";
    s += "<div class='badge'><span class='e'>"+String(bestE,2)+"</span>Energia max J</div>";
    server.sendContent(s);
  }

  // Tabla solo del atleta activo
  server.sendContent(
    "<table><tr><th>#</th><th>Vel(m/s)</th><th>Ang</th><th>Dist(m)</th>"
    "<th>Acel</th><th>t(s)</th><th>E(J)</th><th>P(W)</th><th>Ang?</th></tr>"
  );

  bool hayDatos = false;
  for (int i=0;i<throwLogCount;i++) {
    ThrowRecord& r=throwLog[i];
    if (r.atletaIdx != atletaActivo) continue;
    hayDatos = true;
    const char* ac="bad"; const char* al="Malo";
    if      (r.angle>=32&&r.angle<=39){ac="ok";  al="Optimo";}
    else if (r.angle>=28&&r.angle<32) {ac="warn";al="Bajo";}
    else if (r.angle>39 &&r.angle<=44){ac="warn";al="Alto";}
    s  = "<tr><td>"+String(r.num)+"</td>";
    s += "<td class='v'>"+String(r.velFinal,2)+"</td>";
    s += "<td class='a'>"+String(r.angle,1)+"</td>";
    s += "<td class='d'>"+String(r.distance,2)+"</td>";
    s += "<td>"+String(r.maxAccel,2)+"</td>";
    s += "<td>"+String(r.impulseTime,3)+"</td>";
    s += "<td class='e'>"+String(r.energy,2)+"</td>";
    s += "<td class='p'>"+String(r.power,2)+"</td>";
    s += "<td class='"; s+=ac; s+="'>"; s+=al; s+="</td></tr>";
    server.sendContent(s);
  }
  if (!hayDatos)
    server.sendContent("<tr><td colspan='9' style='color:#334B62;padding:16px'>Sin lanzamientos para este atleta</td></tr>");

  // Botones
  s  = "</table><br>";
  s += "<a class='btn' href='/csv'>&#8595; CSV " + nombreActivo() + "</a>";
  s += "<a class='btn btn-gray' href='/csv?a=Todos'>&#8595; CSV Todos</a>";
  s += "<a class='btn btn-red' href='/reset' onclick=\"return confirm('Borrar lanzamientos de " + nombreActivo() + "?')\">&#215; Reset atleta</a>";
  s += "<a class='btn btn-gray' href='/atletas'>&#9651; Gestionar atletas</a>";
  server.sendContent(s);
  server.sendContent(htmlFooter());
  server.sendContent("");
}

// ================================================================
//  PAGINA ATLETAS  /atletas
// ================================================================
void handleAtletas() {
  server.setContentLength(CONTENT_LENGTH_UNKNOWN);
  server.send(200, "text/html; charset=utf-8", "");
  server.sendContent(htmlHeader("Atletas"));

  String s = "<h1>&#9651; LANCEA &mdash; Atletas</h1>";
  s += "<div class='sub'>Selecciona el atleta activo o registra uno nuevo</div>";
  server.sendContent(s);

  // Lista de atletas con boton seleccionar y borrar
  server.sendContent("<h2>Atletas registrados</h2><table><tr><th>Nombre</th><th>Lanzamientos</th><th>Accion</th></tr>");

  for (int i=0; i<numAtletas; i++) {
    int cnt=0;
    for (int j=0;j<throwLogCount;j++)
      if (throwLog[j].atletaIdx==i) cnt++;

    bool esActivo = (i == atletaActivo);
    s  = "<tr><td>";
    if (esActivo) s += "<span class='atleta-activo'>&#9654; ";
    s += String(atletas[i].nombre);
    if (esActivo) s += " (activo)</span>";
    s += "</td><td>" + String(cnt) + "</td><td>";
    if (!esActivo)
      s += "<a class='btn btn-green' href='/set_atleta?i="+String(i)+"'>Seleccionar</a>";
    else
      s += "<span style='color:#334B62'>Activo</span>";
    if (String(atletas[i].nombre) != "Invitado")
      s += " <a class='btn btn-red' href='/del_atleta?i="+String(i)+"' onclick=\"return confirm('Borrar "+String(atletas[i].nombre)+"?')\">&#215;</a>";
    s += "</td></tr>";
    server.sendContent(s);
  }
  server.sendContent("</table>");

  // Formulario agregar atleta
  s  = "<h2>Registrar nuevo atleta</h2>";
  s += "<form action='/add_atleta' method='post'>";
  s += "<input type='text' name='nombre' placeholder='Nombre del atleta' maxlength='23'>";
  s += " <button class='btn btn-green' type='submit'>+ Registrar</button>";
  s += "</form>";
  server.sendContent(s);

  server.sendContent("<br><a class='btn' href='/'>&#8592; Volver al panel</a>");
  server.sendContent(htmlFooter());
  server.sendContent("");
}

// ================================================================
//  SELECCIONAR ATLETA  /set_atleta?i=N
// ================================================================
void handleSetAtleta() {
  if (server.hasArg("i")) {
    int idx = server.arg("i").toInt();
    seleccionarAtleta(idx);
    safePrintln("[ATLETA] Activo: " + nombreActivo());
  }
  server.sendHeader("Location", "/atletas");
  server.send(302, "text/plain", "");
}

// ================================================================
//  AGREGAR ATLETA  POST /add_atleta
// ================================================================
void handleAddAtleta() {
  if (server.hasArg("nombre")) {
    String nombre = server.arg("nombre");
    int idx = agregarAtleta(nombre);
    if (idx >= 0) {
      seleccionarAtleta(idx);
      safePrintln("[ATLETA] Registrado: " + nombre);
    }
  }
  server.sendHeader("Location", "/atletas");
  server.send(302, "text/plain", "");
}

// ================================================================
//  BORRAR ATLETA  /del_atleta?i=N
//  Solo borra el nombre, sus lanzamientos quedan en RAM
// ================================================================
void handleDelAtleta() {
  if (server.hasArg("i")) {
    int idx = server.arg("i").toInt();
    if (idx > 0 && idx < numAtletas) {  // no borrar Invitado (idx=0)
      // Mover los siguientes una posicion atras
      for (int i=idx; i<numAtletas-1; i++)
        atletas[i] = atletas[i+1];
      numAtletas--;
      // Ajustar referencias en lanzamientos
      for (int i=0;i<throwLogCount;i++) {
        if (throwLog[i].atletaIdx == idx)       throwLog[i].atletaIdx = 0;
        else if (throwLog[i].atletaIdx > idx)   throwLog[i].atletaIdx--;
      }
      if (atletaActivo >= numAtletas) atletaActivo = numAtletas-1;
      if (atletaActivo == idx) atletaActivo = 0;
    }
  }
  server.sendHeader("Location", "/atletas");
  server.send(302, "text/plain", "");
}

// ================================================================
//  CSV  /csv          → atleta activo
//       /csv?a=Todos  → todos
// ================================================================
void handleCSV() {
  int filter = atletaActivo;
  String fname = nombreActivo();
  if (server.hasArg("a") && server.arg("a") == "Todos") {
    filter = -999;
    fname  = "Todos";
  }
  String csv = buildCSV(filter);
  server.sendHeader("Content-Disposition",
    "attachment; filename=\"LANCEA_" + fname + ".csv\"");
  server.send(200, "text/csv; charset=utf-8", csv);
}

String buildCSV(int filterAtleta) {
  String csv = "# LANCEA - Sesion de Lanzamientos\n";
  csv += "# Atleta: " + (filterAtleta==-999 ? String("Todos") : nombreActivo()) + "\n";
  csv += "num,Atleta,Velocidad,Angulo,Distancia,maxAccel,impulseTime,Energia,Potencia\n";
  for (int i=0;i<throwLogCount;i++) {
    ThrowRecord& r=throwLog[i];
    if (filterAtleta != -999 && r.atletaIdx != filterAtleta) continue;
    String aName = (r.atletaIdx>=0 && r.atletaIdx<numAtletas)
                   ? String(atletas[r.atletaIdx].nombre) : "?";
    csv += String(r.num)+","+aName+",";
    csv += String(r.velFinal,2)+","+String(r.angle,1)+",";
    csv += String(r.distance,2)+","+String(r.maxAccel,2)+",";
    csv += String(r.impulseTime,3)+","+String(r.energy,2)+","+String(r.power,2)+"\n";
  }
  return csv;
}

// ================================================================
//  STATUS JSON
// ================================================================
void handleStatus() {
  String json = "{";
  json += "\"throws\":"+String(throwLogCount)+",";
  json += "\"atleta_activo\":\""+nombreActivo()+"\",";
  json += "\"num_atletas\":"+String(numAtletas)+",";
  json += "\"estado\":\"";
  json += estadoActual==IMPULSO?"IMPULSO":estadoActual==PAUSA?"PAUSA":"IDLE";
  json += "\",\"uptime_s\":"+String(millis()/1000)+"}";
  server.send(200, "application/json", json);
}

// ================================================================
//  RESET ATLETA ACTIVO  /reset
// ================================================================
void handleResetAtleta() {
  // Elimina solo los lanzamientos del atleta activo
  int j=0;
  for (int i=0;i<throwLogCount;i++)
    if (throwLog[i].atletaIdx != atletaActivo)
      throwLog[j++] = throwLog[i];
  throwLogCount = j;
  server.sendHeader("Location","/");
  server.send(302,"text/plain","");
}

// ================================================================
//  RESET TOTAL  /resetall
// ================================================================
void handleResetAll() {
  throwLogCount=0; throwCount=0;
  resetVariables(); estadoActual=IDLE;
  server.sendHeader("Location","/");
  server.send(302,"text/plain","");
}

// ================================================================
//  PUBLICAR POR SERIAL
// ================================================================
void publishThrow(double v,double a,double t,double d,double e,double p) {
  safePrintln(""); safePrintln("THROW_START");
  safePrintln("Atleta: "            + nombreActivo());
  safePrint("Lanzamiento #: ");     safePrintln(String(throwCount));
  safePrint("Velocidad: ");         safePrint(String(v,2)); safePrintln(" m/s");
  safePrint("Angulo: ");            safePrint(String(a,1)); safePrintln(" deg");
  safePrint("Distancia: ");         safePrint(String(d,2)); safePrintln(" m");
  safePrint("Aceleracion maxima: ");safePrint(String(maxAccel,2)); safePrintln(" m/s2");
  safePrint("Tiempo de impulso: "); safePrint(String(t,3)); safePrintln(" s");
  safePrint("Energia cinetica: ");  safePrint(String(e,2)); safePrintln(" J");
  safePrint("Potencia: ");          safePrint(String(p,2)); safePrintln(" W");
  safePrintln("THROW_END"); safePrintln("");
}

// ================================================================
//  COMANDOS SERIAL
// ================================================================
void handleCommands() {
  if (!Serial.available()) return;
  String cmd = Serial.readStringUntil('\n'); cmd.trim();
  if (cmd == "DUMP")  handleDump();
  if (cmd == "RESET") handleReset();
}

void handleDump() {
  safePrintln("DUMP_START");
  safePrintln("CSV_HEADER:num,Atleta,Velocidad,Angulo,Distancia,maxAccel,impulseTime,Energia,Potencia");
  for (int i=0;i<throwLogCount;i++) {
    ThrowRecord& r=throwLog[i];
    String aName=(r.atletaIdx>=0&&r.atletaIdx<numAtletas)?String(atletas[r.atletaIdx].nombre):"?";
    String row="CSV_ROW:"+String(r.num)+","+aName+",";
    row+=String(r.velFinal,2)+","+String(r.angle,1)+","+String(r.distance,2)+",";
    row+=String(r.maxAccel,2)+","+String(r.impulseTime,3)+",";
    row+=String(r.energy,2)+","+String(r.power,2);
    safePrintln(row);
  }
  safePrintln("DUMP_END");
}

void handleReset() {
  throwLogCount=0; throwCount=0;
  resetVariables(); estadoActual=IDLE;
  safePrintln("[RESET] Listo para nueva sesion.");
}

void resetVariables() {
  v_x=0;v_y=0;v_z=0;
  ax_f=0;ay_f=0;az_f=0;
  prev_aMag=0;maxAccel=0;launchAngle=0;
}
