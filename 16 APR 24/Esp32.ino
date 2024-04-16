//#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include "Queue.h"
#include <WiFiManager.h>

//
#include "HardwareSerial.h"   //  w/o this, get verbose nastygrams (orange)
#include "DFRobotDFPlayerMini.h"

const char* ssid = "OnePlus";
const char* password = "IOT_proj";

const byte RXD2 = 26; // Connects to module's RX
const byte TXD2 = 27; // Connects to module's TX

HardwareSerial dfSD(1); // Use UART channel 1
DFRobotDFPlayerMini player;

//DynamicJsonDocument doc();

//URL changes with different wifi connections 
String serverName = "http://192.168.101.11:8000/detect";
String server2 = "http://192.168.101.11:5000/detect";

const int trigPin = 14;
const int echoPin = 12;

#define POWER_PIN 32  // ESP32's pin GPIO32 that provides the power to the rain sensor
#define AO_PIN 33  

//define sound speed in cm/uS
#define SOUND_SPEED 0.034
#define CM_TO_INCH 0.393701

long duration;
float distanceCm;
float distanceInch;


Queue<int> queue = Queue<int>(10); // Max 5 chars!

void setup(){
   WiFi.mode(WIFI_STA);
   Serial.begin(115200);
    WiFiManager wm;
   //WiFi.begin(ssid,password);
  //  Serial.println("Connecting");
  //  while(WiFi.status()!=WL_CONNECTED){
  //   delay(500);
  //   Serial.print(".");
  //  }

  //  Serial.println("");

  //  Serial.print("Connected to WiFi network with IP Address: ");
  //  Serial.println(WiFi.localIP());
   wm.resetSettings();
   bool res;
  res = wm.autoConnect("AutoConnectAP","password");
  if(!res) {
        Serial.println("Failed to connect");
        // ESP.restart();
    } 
    else {
        //if you get here you have connected to the WiFi    
        Serial.println("connected...yeey :)");
    }
   // Serial.begin(19200);
  dfSD.begin(9600, SERIAL_8N1, RXD2, TXD2);
  delay(2000);

  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT);
  pinMode(POWER_PIN, OUTPUT); 

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
    delay(500);
    int httpR = http2.GET();

    if(httpResponseCode>0){
      Serial.print("HTTP Response code: ");
      Serial.println(httpResponseCode);
      String payload = http.getString();
      Serial.println(payload);
      // JsonDocument doc;

      DynamicJsonDocument doc(1024);
      deserializeJson(doc, payload);
      Serial.println(payload.length());

//      Serial.println(doc);
      
      for(int i = 0;i<doc.size();i++){
         int index = doc[i]["ind"];
         Serial.println(index);
        //  if(index==0){
        //   break;
        //  }
        if(index==0){
          break;
        }
        
          // player.play(index);
          // delay(2000);
          player.play(index);
          // player.reset();
         
        delay(2000);
      }

      Serial.println("Out of for loop");

      


      // int count = queue.count();

      // while(count--)
      // {
      //   int index = queue.front();
      //   queue.pop();
      //   player.play(index);
      //   Serial.println(index);

      // }
       
//      player.play(index);
    }else{
      Serial.print("Error code: ");
      Serial.println(httpResponseCode);
    }


  if(httpR>0){
      Serial.print("HTTP 2 Response code: ");
      Serial.println(httpR);
      String payload = http2.getString();
      Serial.print("robo_payload: ");
      Serial.println(payload);
      // JsonDocument doc;
      DynamicJsonDocument doc(1024);
      deserializeJson(doc, payload);
      Serial.println(payload.length());

//      Serial.println(doc);
      
      for(int i = 0;i<doc.size();i++){

      
         int index = doc[i]["ind"];
         Serial.println(index);
         if(index==0){
          break;
         }
        //  if(index!=0){
          player.play(index);
          // delay(2000);
          // player.reset();
        //  }
        delay(2000);
      }
       
//         player.play(index);
    }else{
      Serial.print("Error code2: ");
      Serial.println(httpR);
    }
    

    http.end();
    // http2.end();
   }
   else{
    Serial.println("WiFi Disconnected");
   }


   digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  
  // Calculate the distance
  distanceCm = duration * SOUND_SPEED/2;
  
  // Convert to inches
  distanceInch = distanceCm * CM_TO_INCH;
  
  // Prints the distance in the Serial Monitor
  Serial.print("Distance (cm): ");
  Serial.println(distanceCm);
  Serial.print("Distance (inch): ");
  Serial.println(distanceInch);
  
  
  delay(500);


  //needs to be checked 
  digitalWrite(POWER_PIN, HIGH);  // turn the rain sensor's power  ON
  delay(10);                      // wait 10 milliseconds

  int rain_value = analogRead(AO_PIN);
  digitalWrite(POWER_PIN, LOW);  // turn the rain sensor's power OFF

  Serial.print("Rain Value: ");

  Serial.println(rain_value);  // print out the analog value
  delay(500);  
}
