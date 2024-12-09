#include <Arduino.h>
#include <SoftwareSerial.h>
#include "SCD30.h"

// Déclarez SoftwareSerial avec les nouvelles broches : RX sur 5 et TX sur 6
SoftwareSerial xbeeSerial(12, 13);

#if defined(ARDUINO_ARCH_AVR)
    #pragma message("Defined architecture for ARDUINO_ARCH_AVR.")
    #define SERIAL Serial
#elif defined(ARDUINO_ARCH_SAM)
    #pragma message("Defined architecture for ARDUINO_ARCH_SAM.")
    #define SERIAL SerialUSB
#elif defined(ARDUINO_ARCH_SAMD)
    #pragma message("Defined architecture for ARDUINO_ARCH_SAMD.")
    #define SERIAL SerialUSB
#elif defined(ARDUINO_ARCH_STM32F4)
    #pragma message("Defined architecture for ARDUINO_ARCH_STM32F4.")
    #define SERIAL SerialUSB
#else
    #pragma message("Not found any architecture.")
    #define SERIAL Serial
#endif

String moduleID = "AirNode-1"; // ID du module

void setup() {
    Wire.begin();
    SERIAL.begin(9600);
    scd30.initialize();
    xbeeSerial.begin(9600);
    delay(2000); // Attendre 2 secondes pour que le XBee soit prêt
}

void loop() {
    float result[3] = {0};

    if (scd30.isAvailable()) {
        scd30.getCarbonDioxideConcentration(result);
        SERIAL.print("Carbon Dioxide Concentration is: ");
        SERIAL.print(result[0]);
        SERIAL.println(" ppm");
        SERIAL.print("Temperature = ");
        SERIAL.print(result[1]);
        SERIAL.println(" ℃");
        SERIAL.print("Humidity = ");
        SERIAL.print(result[2]);
        SERIAL.println(" %");
        SERIAL.println(" ");

        // Envoyer les données au XBee, CO2, Température et Humidité
        String message = moduleID + "," + String(result[0]) + "," + String(result[1]) + "," + String(result[2]);
        xbeeSerial.println(message);
    }

    // Attendre une réponse du XBee
    /*if (xbeeSerial.available()) {
        SERIAL.println("Available");
        String response = "";
        while (xbeeSerial.available()) {
        char c = xbeeSerial.read();  // Lire chaque caractère reçu
        response += c;               // Ajouter le caractère au message
        }
        SERIAL.print("Réponse du XBee : ");
        SERIAL.println(response);      // Afficher la réponse sur le moniteur série
    }*/

    delay(3000);// Envoie données toutes les 30 secondes
}