#include "MAX30105.h"
#include "heartRate.h"
MAX30105 particleSensor;

long lastBeat = 0; //Time at which the last beat occurred
//initializing start time to ensure 2 min run time 
long starttime = millis();
long endtime = starttime;

void setup() {
  Serial.begin(115200);
  Serial.println("Initializing...");

  // Initialize sensor
  if (!particleSensor.begin(Wire, I2C_SPEED_FAST)) //Use default I2C port, 400kHz speed
  {
    Serial.println("MAX30105 was not found. Please check wiring/power. ");
    while (1);
  }
  Serial.println("Place your index finger on the sensor with steady pressure.");

  particleSensor.setup(); //Configure sensor with default settings
  particleSensor.setPulseAmplitudeRed(0x0A); //Turn Red LED to low to indicate sensor is running
  particleSensor.setPulseAmplitudeGreen(0); //Turn off Green LED


}

void loop() {
 long irValue = particleSensor.getIR();
 if(endtime< 120000){

  if (checkForBeat(irValue) == true)
  {
    //We sensed a beat!
    long delta = millis() - lastBeat;
    lastBeat = millis();

  long beatsPerMinute = 60 / (delta / 1000.0);
  Serial.print("IR=");
  Serial.print(irValue);
  Serial.print(", BPM=");
  Serial.print(beatsPerMinute);
  Serial.println();
  endtime=millis();
  }


 }
}
