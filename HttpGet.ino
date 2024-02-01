#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "PDSIT";
const char* password = "";

String serverName = "http://10.24.20.167:5000/detect";

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
}

void loop(){
   if(WiFi.status()==WL_CONNECTED){
    HTTPClient http;

    String serverPath = serverName;

    http.begin(serverPath.c_str());

    int httpResponseCode = http.GET();

    if(httpResponseCode>0){
      Serial.print("HTTP Response code: ");
      Serial.println(httpResponseCode);
      String payload = http.getString();
      Serial.println(payload);
    }else{
      Serial.print("Error code: ");
      Serial.println(httpResponseCode);
    }

    http.end();
   }
   else{
    Serial.println("WiFi Disconnected");
   }
   delay(10000);
}
