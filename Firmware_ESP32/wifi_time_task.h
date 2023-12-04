#ifndef WIFI_TIME_TASK_H
#define WIFI_TIME_TASK_H

#include <Arduino.h>
#include "global.h"

class WiFi_Time_Task {
  public:
    WiFi_Time_Task();  // Construtor da classe EEPROM_utils
    void start();
    time_t getTimeNow();
    time_t getNow();
    tm TimeInfo();
    bool synchronize();

  private:
    bool synced = false;
    const char* ntpServer = "a.st1.ntp.br";
    const long gmtOffset_sec = -3 * 3600;
    const int daylightOffset_sec = 0;
    time_t now;
    tm time_info;
};
#endif
