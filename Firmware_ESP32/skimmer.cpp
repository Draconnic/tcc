#include "skimmer.h"
#include "global.h"

Skimmer_Task::Skimmer_Task() {}

void Skimmer_Task::start(int level_sensor, int level_sensor_connection) {
  if(level_sensor == 1 || level_sensor_connection == 0){
    digitalWrite(rele, LOW);
  } else {
    digitalWrite(rele, HIGH);
  }
}