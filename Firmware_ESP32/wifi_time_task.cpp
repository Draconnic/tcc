#include "wifi_time_task.h"

#include "global.h"
Server_Config server_config_wifi;
time_t previousMillis = 0;
const time_t interval = 30000;

WiFi_Time_Task::WiFi_Time_Task() {}

void WiFi_Time_Task::start() {
  //Serial.println("Tarefa de conexão do WiFi");
  //Serial.println("-------------------------------------------");
  WiFi.mode(WIFI_STA);
  unsigned long currentMillis = millis();
  if (WiFi.status() == WL_CONNECTED){
    //Serial.println("Conectado ao Wifi");
    if(synced == false) {
      Serial.print("configTime uses ntpServer ");
      Serial.println(ntpServer);
      configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
      Serial.print("synchronising time");
      
      while (time_info.tm_year + 1900 < 2000 ) {
        time(&now);
        localtime_r(&now, &time_info);
        delay(100);
        Serial.print(".");
      }
      Serial.print("\n time synchronsized \n");
      synced = true;
    }
    //Serial.println();
  }
  else if(synced == true && (currentMillis - previousMillis >=interval)) {
    Serial.println("Reconnecting");
    WiFi.disconnect();
    WiFi.reconnect();
    previousMillis = currentMillis;
  }
  else {
    String ssid = server_config_wifi.preference("WiFi_ssid"); 
    String password = server_config_wifi.preference("WiFi_pass");
    Serial.print("Connecting to ");
    Serial.println(ssid);
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
      Serial.print(".");
      delay(500);
    }
    Serial.println("\nConnected to the WiFi network");
    Serial.print("Local ESP32 IP: ");
    Serial.println(WiFi.localIP());
  }
}

time_t WiFi_Time_Task::getNow() {
  return millis() / 1000;
}

time_t WiFi_Time_Task::getTimeNow() {
  if(now == 0){
    return millis() / 1000;
  } else {
    time(&now);
    return now;
  }
}

tm WiFi_Time_Task::TimeInfo() {
  time(&now);
  localtime_r(&now, &time_info);
  return time_info;
}

bool WiFi_Time_Task::synchronize() {
  return synced;
}