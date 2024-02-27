//#include "Arduino.h"
#include "HardwareSerial.h"   //  w/o this, get verbose nastygrams (orange)
#include "DFRobotDFPlayerMini.h"

// Use pins 2 and 3 to communicate with DFPlayer Mini
const byte RXD2 = 26; // Connects to module's RX
const byte TXD2 = 27; // Connects to module's TX

HardwareSerial dfSD(1); // Use UART channel 1
DFRobotDFPlayerMini player;
   
void setup()
{
  Serial.begin(19200);
  dfSD.begin(9600, SERIAL_8N1, RXD2, TXD2);
  delay(2000);

  if (player.begin(dfSD))
  {
    Serial.println("OK");

    // Set volume to maximum (0 to 30).
    player.volume(30); //30 is very loud
  }
  else
  {
    Serial.println("Connecting to DFPlayer Mini failed!");
  }
}

void loop()
{
  Serial.print("Playing #1 \t");
  player.play(1);
  Serial.println("play start");
  delay(20000);
  Serial.println("played 2 sec.");
}
