#ifndef COLLECT_DATA_TASK_H
#define COLLECT_DATA_TASK_H

#include <Arduino.h>
#include "global.h"

class Collect_Data_Task {
  public:
    Collect_Data_Task();  // Construtor da classe EEPROM_utils
    void start(time_t unix_time, tm time_info, bool synchronize);
    String synchronize_func(time_t unix_time, tm time_info, bool synchronize, DynamicJsonDocument &doc);
    bool sensors(String sensor_name);
    float phSensor();
  private:
    time_t previous_seconds = 0;
    const time_t interval = 30;
    String file_name;
    const int rele_skimmer = 13;
    const int level_sensor = 15;
    const int level_sensor_connection = 2;

    // Variáveis pH
    float calibration_value = 20.24 - 0.7; //21.34 - 0.7
    int phval = 0; 
    unsigned long int avgval; 
    int buffer_arr[10],temp;
    float ph_act;
};
#endif
