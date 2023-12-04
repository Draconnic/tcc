#include "server_configs.h"
#include "global.h"


Preferences preferences_config;

IPAddress apIP(192, 168, 27, 1);
DNSServer dnsServer;
AsyncWebServer server(80);

Server_Config::Server_Config() {}

void Server_Config::start() {
  String MAC_Address = MAC_address();
  WiFi.mode(WIFI_AP);
  WiFi.softAPConfig(apIP, apIP, IPAddress(255, 255, 255, 0));
  WiFi.softAP("ESP_" + MAC_Address);

  const byte DNS_PORT = 53;
  dnsServer.start(DNS_PORT, "*", apIP);

  IPAddress myIP = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(myIP);
  Serial.println("Servidor iniciado");

  
  preferences_config.begin("ESP_config", false);
  preferences_config.clear();

  preferences_config.putString("ESP_id", MAC_Address);

  server.onNotFound([](AsyncWebServerRequest *request) {
    // Criação de uma página HTML com um formulário de perguntas
    String html = "<html><head>";
    html += "<style>";
    html += "body { font-family: Arial, sans-serif; text-align: center; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }";
    html += ".container { display: flex; flex-direction: column; align-items: center; }";
    html += ".form-group { margin-bottom: 10px; }";
    html += "label { display: block; margin-bottom: 5px; }";
    html += "input[type='text'] { width: 100%; padding: 5px; }";
    html += "input[type='submit'] { padding: 10px 20px; font-size: 16px; background-color: #4CAF50; color: white; border: none; }";
    html += "@media screen and (min-width: 768px) { .container { max-width: 500px; margin: 0 auto; } }";
    html += "</style>";
    html += "</head><body>";
    html += "<div class='container'>";
    html += "<h1>Caixa de Texto</h1>";
    html += "<h2>Perguntas</h2>";
    html += "<form method='POST' action='/message'>";

    // Primeira pergunta
    html += "<div class='form-group'>";
    html += "<label for='pergunta1'>Pergunta 1:</label>";
    html += "<input type='text' id='pergunta1' name='message1' placeholder='Responda a pergunta 1' />";
    html += "</div>";

    // Segunda pergunta
    html += "<div class='form-group'>";
    html += "<label for='pergunta2'>Pergunta 2:</label>";
    html += "<input type='text' id='pergunta2' name='message2' placeholder='Responda a pergunta 2' />";
    html += "</div>";

    // Terceira pergunta
    html += "<div class='form-group'>";
    html += "<label for='pergunta3'>Pergunta 3:</label>";
    html += "<input type='text' id='pergunta3' name='message3' placeholder='Responda a pergunta 3' />";
    html += "</div>";

    // Botão de enviar
    html += "<input type='submit' value='Enviar'>";

    html += "</form>";
    html += "</div>";
    html += "</body></html>";
    request->send(200, "text/html", html);
  });
  server.on("/message", [](AsyncWebServerRequest * request) {
    String message = "";
    if (request->hasParam("message1", true)) {
      message = request->getParam("message1", true)->value();
      Serial.println("Mensagem recebida: " + message);
      preferences_config.putString("WiFi_ssid", message);
    }
    if (request->hasParam("message2", true)) {
      message = request->getParam("message2", true)->value();
      Serial.println("Mensagem recebida: " + message);
      preferences_config.putString("WiFi_pass", message);
    }
    if (request->hasParam("message3", true)) {
      message = request->getParam("message3", true)->value();
      Serial.println("Mensagem recebida: " + message);
      preferences_config.putString("Machine_id", message);

    }
    preferences_config.end();
    AsyncWebServerResponse *response = request->beginResponse(200, "text/html", "<h1>Mensagem recebida com sucesso!</h1>");
    request->send(response);
    ESP.restart();                     // Reinicia o ESP
  });
  server.begin();                      // Inicia o servidor web
  while(1){
    dnsServer.processNextRequest();
  }

}

String Server_Config::MAC_address() {
  String macAddress = WiFi.macAddress();  // Obtém o endereço MAC do ESP
  macAddress.replace(":", "");
  macAddress.toLowerCase();
  return macAddress;
}

void Server_Config::reset() {
  preferences_config.begin("ESP_config", false);
  preferences_config.clear();
  preferences_config.end();
}

bool Server_Config::condition() {
  String ESP_id = preference("ESP_id"); 
  String Machine_id = preference("Machine_id");
  String WiFi_ssid = preference("WiFi_ssid"); 
  String WiFi_pass = preference("WiFi_pass");
  Serial.println(ESP_id);
  Serial.println(Machine_id);
  Serial.println(WiFi_ssid);
  Serial.println(WiFi_pass);
  if (ESP_id != "" && Machine_id != "" && WiFi_ssid != "" && WiFi_pass != ""){
    return true;
  }
  else{
    return false;
  }
}

String Server_Config::preference(String name) {
  preferences_config.begin("ESP_config", true);
  String ESP_id = preferences_config.getString("ESP_id"); 
  String Machine_id = preferences_config.getString("Machine_id");
  String WiFi_ssid = preferences_config.getString("WiFi_ssid"); 
  String WiFi_pass = preferences_config.getString("WiFi_pass");
  preferences_config.end();
  if (name == "ESP_id") {
      return ESP_id;
  } else if (name == "Machine_id") {
      return Machine_id;
  } else if (name == "WiFi_ssid") {
      return WiFi_ssid;
  } else if (name == "WiFi_pass") {
      return WiFi_pass;
  }
}
