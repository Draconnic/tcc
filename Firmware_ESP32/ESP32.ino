/*
Coisas a adiconar 
- Código do PH
  {https://www.electroniclinic.com/esp32-ph-sensor-iot-ph-sensor-code-and-circuit-diagram/}
- Função de Reset
  {
    Reiniciou o dispositivo
    Conector do tanque desplugado (0)
    Ativar wifi com uma aba de configuração
    Ninguem se conectou por 1m30s, continua tarefa
    Se conectou e trocou a senha reiniciar esp com nova senha salva
  }
- Alertas para o usuário




*/


#include "global.h"

WiFi_Time_Task wifi_time_task;
Server_Config server_config;
API_Task api_task;
Collect_Data_Task collect_data_task;
Skimmer_Task skimmer_task;
Preferences preferences;


TaskHandle_t WiFiTimeTask;
TaskHandle_t APITask;
TaskHandle_t CollectDataTask;

const int pH_sensor = 4;
const int skimmer = 17;
const int output2 = 13;
const int level_sensor = 15;
const int level_sensor_connection = 16;

void WiFiTimeTaskCode(void *pvParameters) {
  while (1) {
    wifi_time_task.start();
    delay(3000);
  }
}

void APITaskCode(void *pvParameters) {
  while (1) {
    if (wifi_time_task.synchronize() == true && SD.begin()) {
      time_t unix_time = wifi_time_task.getTimeNow();
      time_t millis_now = wifi_time_task.getNow();
      api_task.start(unix_time, millis_now);
    }
    delay(1000);
  }
}

void CollectDataTaskCode(void *pvParameters) {
  while (1) {
    if (SD.begin()) {
      time_t unix_time = wifi_time_task.getTimeNow();
      tm time_info = wifi_time_task.TimeInfo();
      bool synchronize = wifi_time_task.synchronize();
      collect_data_task.start(unix_time, time_info, synchronize);
    }
    delay(1000);
  }
}

void SkimmerTaskCode(void *pvParameters) {
  while (1) {
    int value_level_sensor = digitalRead(level_sensor); 
    int value_level_sensor_connection = digitalRead(level_sensor_connection);
    skimmer_task.start(value_level_sensor, value_level_sensor_connection);
    delay(1000);
  }
}


void setup() {
  Serial.begin(115200);
  delay(3000);
  pinMode(pH_sensor, INPUT);
  pinMode(skimmer, OUTPUT);
  pinMode(output2, OUTPUT);
  pinMode(level_sensor, INPUT_PULLDOWN);
  pinMode(level_sensor_connection, INPUT_PULLDOWN);
  // if (Aba de configuração == true) { Abrei wifi, para configurar - while} 
  if (server_config.condition() == true) {
    Serial.println("Executando Multitarefas");
    xTaskCreatePinnedToCore(SkimmerTaskCode, "SkimmerTask", 1250, NULL, 1, &WiFiTimeTask, 0);
    xTaskCreatePinnedToCore(WiFiTimeTaskCode, "WiFiTimeTask", 3000, NULL, 2, &WiFiTimeTask, 0);
    //delay(7000);
    //xTaskCreatePinnedToCore(APITaskCode, "APITask", 5000, NULL, 1, &APITask, 1);
    //xTaskCreatePinnedToCore(CollectDataTaskCode, "CollectDataTask", 4500, NULL, 2, &CollectDataTask, 1);`
    
  } else {
    server_config.start();
  }
}

void loop() {
  // O loop não é necessário quando se usa o FreeRTOS
}
