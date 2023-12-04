#include "api_task.h"
#include "global.h"

Server_Config server_config_api;
int http_code = 0;
API_Task::API_Task() {}

void API_Task::start(time_t unix_time, time_t millis_now) {
  Serial.println("Tarefa da API");
  Serial.println("-------------------------------------------");
  File root = SD.open("/");
  if (!root) {
    Serial.println("Failed to open root directory");
    return;
  }
  Serial.println("Acesso ao diretetório: /");
  if (!SD.exists("/dados_enviados")) {
      SD.mkdir("/dados_enviados");
  }
  Serial.println("Pasta /dados_enviados já existe");
  File file = root.openNextFile();
  while (file) {
    if (WiFi.status() != WL_CONNECTED) {
      break;
    }

    if (!file.isDirectory()) {
      Serial.println("Arquivo:" + String(file.name()));
      String fileData = "";
      while (file.available()) {
        char data =  file.read();
        fileData += data;
      }
      DynamicJsonDocument doc(1024);
      DeserializationError error = deserializeJson(doc, fileData);

      if (error) {
        Serial.print(F("Erro no parse do JSON: "));
        Serial.println(error.c_str());
        return;
      }
      http_code = post(doc, unix_time, millis_now);
      Serial.println(http_code);
      if(http_code == 201){
        SD.rename("/" +String(file.name()), "/dados_enviados/" +String(file.name()));
      }
    }
    file = root.openNextFile();
    delay(1000);
  }
  root.close();
  Serial.println();
}

int API_Task::post(DynamicJsonDocument doc, time_t unix_time, time_t millis_now) {
  bool synchronize = doc["synchronize"];
  if (synchronize == false) {
    time_t date_time = doc["date_time"];
    time_t date_task = millis_now - date_time;
    if (date_task >= 0) {
      date_task = unix_time - date_task;
    } else {
      return 0;
    }
    struct tm *tm_info;
    tm_info = gmtime(&date_task);
    char formatted_time[30];
    strftime(formatted_time, sizeof(formatted_time), "%Y-%m-%dT%H:%M:%SZ", tm_info);
    doc["date_time"] = formatted_time;
  }
  doc.remove("synchronize");
  Serial.println("REQUEST - POST: device_registration");
  String access_token = http_request_device_registration(); // 200 - token
  if (access_token != "") {
    return http_request_data(access_token, doc); // 201
  }
  Serial.println("NADA");
  return 0; //;
}

String API_Task::http_request_device_registration(){
  HTTPClient http;
  WiFiClient client;
  StaticJsonDocument<1024> jsonDocument;
  String serverUrl = "http://10.45.68.131:5000/login/device_registration";
  String token_refresh = "";
  String esp_id = server_config_api.preference("ESP_id"); 
  String machine_id = server_config_api.preference("Machine_id");
  Serial.println("Dados registrados");

  if (http.begin(client, serverUrl)) {
    Serial.println("Acesso a url");
    http.addHeader("accept", "application/json");
    Serial.println("Header - accept");
    http.addHeader("Authorization", "Bearer " + token_refresh); // Substitua com seu token
    Serial.println("Header - Authorization");
    http.addHeader("Content-Type", "application/x-www-form-urlencoded");
    String postData = "chip_id=" + esp_id + "&machine=" + machine_id + "&company=finetornos&segredo=secret";
    Serial.println(postData);
    Serial.println("Requisitando post");
    int httpCode = http.POST(postData);
    Serial.println(String(httpCode));
    if (httpCode > 0) {
      if(httpCode == 200) {
        String response = http.getString();
        deserializeJson(jsonDocument, response);
        return jsonDocument["access_token"];
      } else {
        return "";
      }   
    }else {
      return "";
    }
  } else {
    Serial.println("Puts, sem acesso a url");
    return "";
  }
}

int API_Task::http_request_data(String access_token, DynamicJsonDocument doc){
  HTTPClient http;
  WiFiClient client;
  String serverUrl = "http://10.45.68.131:5000/data/insert";

  if (WiFi.status() == WL_CONNECTED && http.begin(client, serverUrl)) {
    http.addHeader("accept", "application/json");
    http.addHeader("Authorization", "Bearer " + access_token); // Substitua com seu token
    http.addHeader("Content-Type", "application/json");
    String jsonString;
    serializeJson(doc, jsonString);
    Serial.println(access_token);
    Serial.println(jsonString);
    return http.POST(jsonString);
    
  }
}

