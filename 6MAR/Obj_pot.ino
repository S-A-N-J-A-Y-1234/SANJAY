#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
//
#include "HardwareSerial.h"   //  w/o this, get verbose nastygrams (orange)
#include "DFRobotDFPlayerMini.h"

const char* ssid = "PDSIT";
const char* password = "";

const byte RXD2 = 26; // Connects to module's RX
const byte TXD2 = 27; // Connects to module's TX

HardwareSerial dfSD(1); // Use UART channel 1
DFRobotDFPlayerMini player;

//DynamicJsonDocument doc();


String serverName = "http://10.24.20.149:5000/detect";
String server2 = "http://10.24.20.167:5000/detect";

void setup(){
   Serial.begin(115200);

   WiFi.begin(ssid,password);
   Serial.println("Connecting");
   while(WiFi.status()!=WL_CONNECTED){
    delay(500);
    Serial.print(".");
   }

   Serial.println("");

   Serial.print("Connected to WiFi network with IP Address: ");
   Serial.println(WiFi.localIP());

   // Serial.begin(19200);
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

void loop(){
   if(WiFi.status()==WL_CONNECTED){
    HTTPClient http;
    HTTPClient http2;

    String serverPath = serverName;
    String serverPath2 = server2;

    http.begin(serverPath.c_str());
    http2.begin(serverPath2.c_str());

    int httpResponseCode = http.GET();
    int httpR = http2.GET();

    if(httpResponseCode>0){
      Serial.print("HTTP Response code: ");
      Serial.println(httpResponseCode);
      String payload = http.getString();
      Serial.println(payload);
      JsonDocument doc;
      deserializeJson(doc, payload);
      Serial.println(payload.length());

//      Serial.println(doc);
      
      for(int i = 0;i<payload.length();i++){
         int index = doc[i]["ind"];
         Serial.println(index);
         if(index==0){
          break;
         }
         if(index!=0){
          player.play(index);
         }
//         delay(2000);
      }
       
//      player.play(index);
    }else{
      Serial.print("Error code: ");
      Serial.println(httpResponseCode);
    }


  if(httpR>0){
      Serial.print("HTTP Response code: ");
      Serial.println(httpR);
      String payload = http2.getString();
      Serial.print("robo_payload: ");
      Serial.println(payload);
      JsonDocument doc;
      deserializeJson(doc, payload);
      Serial.println(payload.length());

//      Serial.println(doc);
      
      for(int i = 0;i<payload.length();i++){
         int index = doc[i]["ind"];
         Serial.println(index);
         if(index==0){
          break;
         }
         if(index!=0){
          player.play(index);
         }
        delay(2000);
      }
       
//         player.play(index);
    }else{
      Serial.print("Error code2: ");
      Serial.println(httpR);
    }
    

    http.end();
    http2.end();
   }
   else{
    Serial.println("WiFi Disconnected");
   }
//   delay(2000);
}
