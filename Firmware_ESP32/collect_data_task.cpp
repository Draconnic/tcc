#include "collect_data_task.h"
#include "global.h"

Collect_Data_Task::Collect_Data_Task() {}

void Collect_Data_Task::start(time_t unix_time, tm time_info, bool synchronize) {
    Serial.println("Tarefa da Coleta de Dados");
    Serial.println("-------------------------------------------");
    DynamicJsonDocument doc(230);
    String jsonString = synchronize_func(unix_time, time_info, synchronize, doc);
    if (jsonString != "pass") {
        Serial.println(jsonString);
        Serial.println("/data_" + file_name + ".json");
        File file = SD.open("/data_" + file_name + ".json", FILE_WRITE);
        if (!file) {
            Serial.println("Failed to open file for writing");
        }
        file.println(jsonString);
        file.close();
    }
    Serial.println();
}

String Collect_Data_Task::synchronize_func(time_t unix_time, tm time_info, bool synchronize, DynamicJsonDocument &doc) {
  Serial.println("Validação da hora");
  if (synchronize == true && (time_info.tm_sec == 30 || time_info.tm_sec == 0)) {
      struct tm *tm_info;
      tm_info = gmtime(&unix_time);
      char formatted_time[30];
      strftime(formatted_time, sizeof(formatted_time), "%Y-%m-%dT%H:%M:%SZ", tm_info);

      doc["date_time"] = formatted_time;
      doc["synchronize"] = synchronize;
      
      char file_name_time[30];
      strftime(file_name_time, sizeof(file_name_time), "%Y-%m-%d_%H-%M-%S", tm_info);
      file_name = file_name_time;
  }
  else if (synchronize == false && unix_time - previous_seconds >= interval) {
      previous_seconds = unix_time;
      doc["date_time"] = unix_time;
      doc["synchronize"] = synchronize;
      file_name = unix_time;
  } else {
    Serial.println("Não deu Horário");
    return "pass";
  }
  
  JsonObject properties = doc.createNestedObject("properties");
  properties["bubbler"]["state"] = sensors("bubbler");
  properties["level_sensor"]["connected_state"] = sensors("level_sensor");
  properties["level_sensor"]["sensor_state"] = sensors("level_sensor_state");
  properties["ph_sensor"]["value"] = phSensor();
  properties["skimmer"] = JsonObject();
  properties["skimmer"]["state"] = sensors("skimmer");
  String jsonString;
  serializeJson(doc, jsonString);
  return jsonString;
}

bool Collect_Data_Task::sensors(String sensor_name) {
  if (sensor_name == "bubbler") {
      return true;
  } else if (sensor_name == "level_sensor") {
      return digitalRead(level_sensor);
  } else if (sensor_name == "level_sensor_state") {
      return digitalRead(level_sensor_connection);
  } else if (sensor_name == "skimmer") {
      return digitalRead(rele_skimmer);
  }
}

float Collect_Data_Task::phSensor() {
 // Initiates SimpleTimer
  int quantity = 10;
  for(int i=0;i<quantity;i++) { 
    buffer_arr[i]=analogRead(4);
    delay(30);
  }
  for(int i=0;i<(quantity - 1);i++)  {
    for(int j=i+1;j<quantity;j++) {
      if(buffer_arr[i]>buffer_arr[j]) {
        temp=buffer_arr[i];
        buffer_arr[i]=buffer_arr[j];
        buffer_arr[j]=temp;
      }
    }
  }
  avgval=0;
  for(int i=2;i<8;i++) avgval+=buffer_arr[i];
  float volt=(float)avgval*3.3/4096.0/6;  
  ph_act = -5.70 * volt + calibration_value;
  if (ph_act <= 4.00 || ph_act >= 9.00) {
    // Aviso
  }
  return ph_act;
}

