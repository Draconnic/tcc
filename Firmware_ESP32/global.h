#ifndef GLOBALS_H

#define GLOBALS_H
#include <time.h>
// Libraries - Arduino:
#include <Arduino.h>
#include <ArduinoJson.h>
#include "FS.h"
#include "SD.h"
#include "SPI.h"

#include <freertos/FreeRTOS.h>
#include <freertos/task.h>


// Libraries - WiFi:
#include <WiFi.h>
#include <HTTPClient.h>
#include <WiFiClient.h>
#include <AsyncTCP.h>
#include <ESPAsyncWebServer.h>
#include <NTPClient.h>
#include <DNSServer.h>
#include <WiFiUdp.h>
// Libraries - EEPROM:
#include <Preferences.h>
// Classes 
#include "server_configs.h"
#include "api_task.h"
#include "wifi_time_task.h"
#include "collect_data_task.h"
#include "skimmer.h"

struct Pin_Config {};


#endif