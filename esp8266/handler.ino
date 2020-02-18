//libs
#include <ESP8266WiFi.h>
#include <WiFiClientSecure.h>
#include <ESP8266WebServer.h>
#include <ESP8266HTTPClient.h>
#include <Adafruit_NeoPixel.h>
#include <ArduinoJson.h>

//defines
#define NUM_LEDS 46
#define PIN D1

//host const
const char* host = "https://andrik154.xyz:5000/lampreq";

//wifi sets
const char* ssid = "KV-28";
const char* pass = "5vri4PwI";

//json format
const char* input="{\n\"id\": \"ac1c2170-93a23e6b-93874ca4-363366aa_5\",\n  \"effect\": \"None\",\n  \"color\": 4442398,\n  \"brightness\": \"None\"\n}";

//payload and id-storing string
String payload;
String idc;

const int hb = 180;
const int lb = 40;

Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUM_LEDS, PIN, NEO_GRB+NEO_KHZ800);


void setup() {
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT); 
  digitalWrite(LED_BUILTIN, LOW);
  WiFi.begin(ssid,pass);
  Serial.println("Connecting to ");
  Serial.print(ssid);
  while (WiFi.status() != WL_CONNECTED){
    delay (1000);
    Serial.print(".");
  }
  Serial.print("\nCONNECTED ");
  Serial.println(ssid);

  strip.begin();
  strip.setBrightness(100);
  strip.show();
  digitalWrite(LED_BUILTIN, HIGH);
  
}

void loop() {

  String data = callhttps();
  Serial.println(data);
  DynamicJsonDocument doc(200);
  deserializeJson(doc,data);
  unsigned int color = doc["color"];
  String id = doc["id"];
  String effect = doc["effect"];
  String br = doc["brightness"];
  
  Serial.println(color);
  digitalWrite(LED_BUILTIN, HIGH);

  if (idc!=id){
    if (effect!="None"){
    
    }
    if (br!="None"){
      int cb = strip.getBrightness();
      if (br=="u"){
        if (cb<hb){
          strip.setBrightness(cb+20);
        }
      }
      if (br=="d"){
        if (cb>lb){
          strip.setBrightness(cb-20);
        }
      }
    }
    setColor(color);
  }
  strip.show();
  delay(10000);
}


void setColor(unsigned int color){
  /*for (int i=0; i<NUM_LEDS; i++){
    strip.setPixelColor(i, color);
  }
    strip.show();*/
  strip.fill(color);
  strip.show();
}

void setEffect(String effect){
  
}


String callhttps(){
    digitalWrite(LED_BUILTIN, LOW);
    HTTPClient http;
    http.begin(host, "07:F5:09:A6:B2:F8:48:CE:DF:8E:AD:7C:A4:CC:D2:3F:12:06:DE:CB");
    int httpCode = http.GET();
    if (httpCode >0) {
      payload=http.getString();
      Serial.println("Got payload");
    } else { Serial.print("\n error");
    Serial.println(http.errorToString(httpCode).c_str());
    }
    http.end();
    /*int i=0;
    while (i < payload.length()) {
      i = payload.find('\n', i);
      if (i == std::string:npos) {
        break;
      }
    payload.erase(i);
    }*/
    //payload.trim();
    return payload;
}
  
