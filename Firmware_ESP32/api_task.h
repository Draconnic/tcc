#ifndef API_TASK_H
#define API_TASK_H

#include "global.h"
#include <Arduino.h>

class API_Task {
  public:
    API_Task();
    void start(time_t unix_time, time_t millis_now);
    int post(DynamicJsonDocument doc, time_t unix_time, time_t millis_now);
    String http_request_device_registration();
    int http_request_data(String access_token, DynamicJsonDocument doc);
  private:
    // Nenhum membro privado neste exemplo
};
#endif
