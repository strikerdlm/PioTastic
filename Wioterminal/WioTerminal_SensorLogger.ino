/*
 * WioTerminal_SensorLogger.ino
 * 
 * Description: Combines sensor readings (BME680, Multichannel Gas) 
 *              with RTC timestamping, displays data on TFT, and logs 
 *              to SD card every 5 minutes on the Wio Terminal.
 *              
 * Assumes:
 *  - Wio Terminal Board Support Package installed.
 *  - Required libraries installed (TFT_eSPI, Seeed_BME680, 
 *    Multichannel_Gas_GMXXX, RTC_SAMD51, SD, SPI, Wire).
 *  - BME680 connected via I2C (default addr 0x76 or 0x77).
 *  - Multichannel Gas Sensor v2 connected via I2C (default addr 0x08).
 *  - SD card inserted and formatted (FAT32).
 *  
 * Date: 2024-07-26
 */

// --- Includes ---
#include <SPI.h>                // For SD card
#include <SD.h>                 // For SD card
#include <TFT_eSPI.h>           // For TFT Display
#include "RTC_SAMD51.h"         // For Real Time Clock
#include <Wire.h>               // For I2C communication
#include "seeed_bme680.h"       // For BME680 Sensor
#include <Multichannel_Gas_GMXXX.h> // For Multichannel Gas Sensor
#include <fcntl.h>              // Required for O_APPEND etc.

// --- Definitions ---
#define BME680_I2C_ADDR   (0x77)  // Default BME680 I2C address (can be 0x76 or 0x77)
#define MGS_I2C_ADDR      (0x08)  // Default Multichannel Gas Sensor I2C address
#define SD_CS_PIN         (4)     // Chip Select pin for SD card on Wio Terminal is Pin 4
#define LOG_INTERVAL_MS   (5 * 60 * 1000) // Log every 5 minutes (in milliseconds)
#define LOG_FILENAME      "datalog.csv"

// --- Global Objects ---
TFT_eSPI tft;                   // TFT display object
RTC_SAMD51 rtc;                 // RTC object
Seeed_BME680 bme680((uint8_t)BME680_I2C_ADDR); // BME680 sensor object (I2C)
GAS_GMXXX<TwoWire> gas;         // Multichannel Gas sensor object (Hardware I2C)
File logFile;                   // File object for SD card logging
unsigned long lastLogTime = 0;  // Variable to store the last log time

// --- Setup Function ---
void setup() {
    Serial.begin(115200);
    // while (!Serial); // Optional: wait for serial connection
    Serial.println("Wio Terminal Sensor Logger Starting...");

    // Initialize TFT Display
    tft.init();
    tft.setRotation(3); // Adjust rotation as needed (landscape)
    tft.fillScreen(TFT_BLACK);
    tft.setTextColor(TFT_WHITE, TFT_BLACK);
    tft.setTextSize(2);
    tft.setCursor(10, 10);
    tft.println("Initializing...");

    // Initialize I2C
    Wire.begin();

    // Initialize BME680
    tft.setCursor(10, 30);
    tft.print("BME680: ");
    if (!bme680.init()) {
        Serial.println("BME680 init failed!");
        tft.setTextColor(TFT_RED, TFT_BLACK);
        tft.println("Failed!");
        while (1); // Halt execution
    } else {
        Serial.println("BME680 Initialized.");
        tft.setTextColor(TFT_GREEN, TFT_BLACK);
        tft.println("OK");
    }
    tft.setTextColor(TFT_WHITE, TFT_BLACK); // Reset color

    // Initialize Multichannel Gas Sensor
    tft.setCursor(10, 50);
    tft.print("MGS:    ");
    // Note: gas.begin() does not return a status in this library
    gas.begin(Wire, MGS_I2C_ADDR);
    // We assume initialization succeeded. Error handling might be needed
    // based on sensor readings if issues occur.
    Serial.println("Multichannel Gas Sensor Initialized (assumed OK).");
    tft.setTextColor(TFT_GREEN, TFT_BLACK);
    tft.println("OK");
    // gas.powerOn(); // Power on the heater if needed (check sensor datasheet)

    tft.setTextColor(TFT_WHITE, TFT_BLACK); // Reset color

    // Initialize RTC
    tft.setCursor(10, 70);
    tft.print("RTC:    ");
    rtc.begin();
    // Optional: Set RTC time if needed (e.g., from compilation time or NTP)
    // Example: rtc.adjust(DateTime(F(__DATE__), F(__TIME__))); 
    // Or check if time is valid:
    if (!rtc.now().isValid()) {
        Serial.println("RTC not set! Please set the time.");
        tft.setTextColor(TFT_YELLOW, TFT_BLACK);
        tft.println("Not Set!");
        // Consider setting a default time or waiting for user input/NTP sync
        // rtc.adjust(DateTime(2024, 7, 26, 0, 0, 0)); // Example default
    } else {
        Serial.println("RTC Initialized.");
        tft.setTextColor(TFT_GREEN, TFT_BLACK);
        tft.println("OK");
    }
    tft.setTextColor(TFT_WHITE, TFT_BLACK); // Reset color

    // Initialize SD Card
    tft.setCursor(10, 90);
    tft.print("SD Card:");
    if (!SD.begin(SD_CS_PIN)) {
        Serial.println("SD Card initialization failed!");
        tft.setTextColor(TFT_RED, TFT_BLACK);
        tft.println("Failed!");
        // You might want to allow operation without SD card, depending on requirements
        // while(1); // Halt if SD is critical
    } else {
        Serial.println("SD Card Initialized.");
        tft.setTextColor(TFT_GREEN, TFT_BLACK);
        tft.println("OK");
        
        // Check if log file exists, create header if not
        if (!SD.exists(LOG_FILENAME)) {
            Serial.println("Log file not found, creating header.");
            logFile = SD.open(LOG_FILENAME, FILE_WRITE);
            if (logFile) {
                logFile.println("Timestamp,Temp_C,Pressure_KPa,Humidity_%,Gas_kOhm,NO2_V,C2H5OH_V,VOC_V,CO_V");
                logFile.close();
                Serial.println("Log file header written.");
            } else {
                Serial.println("Error creating log file header!");
                tft.setCursor(120, 90);
                tft.setTextColor(TFT_RED, TFT_BLACK);
                tft.println("Log Err!");
            }
        } else {
            Serial.println("Log file found.");
        }
    }
    tft.setTextColor(TFT_WHITE, TFT_BLACK); // Reset color

    delay(2000); // Wait a bit before starting the loop
    tft.fillScreen(TFT_BLACK); // Clear initialization screen
    tft.setTextSize(2); 
}

// --- Loop Function ---
void loop() {
    unsigned long currentMillis = millis();

    // --- Read Sensors ---
    float tempC = 0.0, pressureKPa = 0.0, humidity = 0.0, gasKohms = 0.0;
    float no2V = 0.0, c2h5ohV = 0.0, vocV = 0.0, coV = 0.0;

    // Read BME680
    if (bme680.read_sensor_data()) {
        Serial.println("Failed to read BME680 data");
        // Handle error - maybe display old data or an error message
    } else {
        tempC = bme680.sensor_result_value.temperature;
        pressureKPa = bme680.sensor_result_value.pressure / 1000.0;
        humidity = bme680.sensor_result_value.humidity;
        gasKohms = bme680.sensor_result_value.gas / 1000.0;
    }

    // Read Multichannel Gas Sensor (Voltage readings)
    no2V = gas.calcVol(gas.measure_NO2());
    c2h5ohV = gas.calcVol(gas.measure_C2H5OH());
    vocV = gas.calcVol(gas.measure_VOC());
    coV = gas.calcVol(gas.measure_CO());

    // --- Get Time ---
    DateTime now = rtc.now();
    char timestamp[25]; // Buffer for "YYYY-MM-DD HH:MM:SS"
    sprintf(timestamp, "%04d-%02d-%02d %02d:%02d:%02d", 
            now.year(), now.month(), now.day(), 
            now.hour(), now.minute(), now.second());

    // --- Display Data on TFT ---
    tft.fillScreen(TFT_BLACK); // Clear screen each update cycle
    tft.setCursor(0, 0);
    tft.setTextSize(2);
    tft.setTextColor(TFT_CYAN, TFT_BLACK);
    tft.println(timestamp); // Display current time
    
    tft.setTextColor(TFT_WHITE, TFT_BLACK);
    tft.setTextSize(2);
    
    // Display BME680 Data
    tft.setCursor(0, 30); tft.printf("Temp: %.1f C", tempC);
    tft.setCursor(0, 55); tft.printf("Pres: %.1f KPa", pressureKPa);
    tft.setCursor(0, 80); tft.printf("Humi: %.1f %%", humidity);
    tft.setCursor(0, 105); tft.printf("GasR: %.1f KOhm", gasKohms);

    // Display Multichannel Gas Data (Voltage)
    tft.setTextColor(TFT_YELLOW, TFT_BLACK);
    tft.setCursor(0, 135); tft.printf("NO2 : %.2f V", no2V);
    tft.setCursor(0, 160); tft.printf("EtOH: %.2f V", c2h5ohV); // Ethanol
    tft.setCursor(0, 185); tft.printf("VOC : %.2f V", vocV);
    tft.setCursor(0, 210); tft.printf("CO  : %.2f V", coV);

    // --- Log Data (if interval passed) ---
    if (currentMillis - lastLogTime >= LOG_INTERVAL_MS) {
        lastLogTime = currentMillis; // Update last log time

        Serial.print("Logging data at: "); Serial.println(timestamp);
        tft.setTextColor(TFT_GREEN, TFT_BLACK);
        tft.setCursor(240, 210); // Position for logging indicator
        tft.setTextSize(1);
        tft.print("Logging...");

        // Format data string for CSV
        char logData[200];
        sprintf(logData, "%s,%.2f,%.2f,%.1f,%.2f,%.3f,%.3f,%.3f,%.3f",
                timestamp, tempC, pressureKPa, humidity, gasKohms,
                no2V, c2h5ohV, vocV, coV);

        // Open file in append mode
        // Use O_APPEND and O_WRITE flags for standard SD library
        logFile = SD.open(LOG_FILENAME, O_APPEND | O_WRITE);
        if (logFile) {
            logFile.println(logData);
            logFile.close(); // Close file immediately after writing
            Serial.println("Data logged successfully.");
            tft.setTextColor(TFT_GREEN, TFT_BLACK);
            tft.setCursor(240, 225);
            tft.print("Logged OK");
        } else {
            Serial.println("Error opening log file for appending!");
            tft.setTextColor(TFT_RED, TFT_BLACK);
            tft.setCursor(240, 225);
            tft.print("Log FAIL");
            // Consider adding more robust error handling here
        }
        tft.setTextColor(TFT_WHITE, TFT_BLACK); // Reset color
        tft.setTextSize(2); // Reset text size
    }

    delay(1000); // Update sensors and display roughly every second
}

// --- Helper Functions (if any) ---
// None needed for this basic version 