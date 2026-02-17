#include <Arduino.h>

// Archivo de prueba para validar el flujo de trabajo en GitHub
// Autor: Joseph Gutierrez
// Fecha: Febrero 2026

void setup() {
    // Inicializar comunicación serie
    Serial.begin(115200);
    Serial.println("--- INICIANDO TEST DE SENSOR ---");
    Serial.println("Estado: Configuración completada.");
}

void loop() {
    // Simular lectura de datos del sensor BNO055
    float aceleracion_x = random(0, 100) / 10.0;
    
    Serial.print("Lectura simulada Accel X: ");
    Serial.print(aceleracion_x);
    Serial.println(" m/s^2");
    
    // Esperar un segundo
    delay(1000);
}
