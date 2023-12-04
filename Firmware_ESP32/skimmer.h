#ifndef SKIMMER_TASK_H
#define SKIMMER_TASK_H

#include <Arduino.h>
#include "global.h"

class Skimmer_Task {
  public:
    Skimmer_Task();
    void start(int level_sensor, int level_sensor_connection);
  private:
  const int rele = 13;
};
#endif
