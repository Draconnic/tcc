#ifndef SERVER_CONFIG_H
#define SERVER_CONFIG_H

#include <Arduino.h>


class Server_Config {
  public:
    Server_Config();
    void start();
    bool condition();
    String preference(String name);
    void reset();
    String MAC_address();
    String data();
  private:

};

#endif
