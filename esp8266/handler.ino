//andrik154

#include <ESP8266WiFi.h>
#include <WiFiClientSecure.h>
#include <ESP8266WebServer.h>
#include <ESP8266HTTPClient.h>
#include <Adafruit_NeoPixel.h>
#include <ArduinoJson.h>
//#include <Ticker.h>

#define NUM_LEDS 42
#define PIN D2

const char* host = "https://andrik154.xyz:5000/lampreq";
const String fingerprint = "07:F5:09:A6:B2:F8:48:CE:DF:8E:AD:7C:A4:CC:D2:3F:12:06:DE:CB";

const char* ssid = "KV-28";
const char* pass = "5vri4PwI";

String data;
String payload;
String id;
String id_old;
int brightness;
String effect;

Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUM_LEDS, PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
  //wifi
  strip.begin();
  
  connectWIFI();
  digitalWrite(LED_BUILTIN, HIGH);
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("Lost WiFi connection");
    connectWIFI();
  } 
  data=callhttps();
  DynamicJsonDocument doc(200);
  deserializeJson(doc, data);
  unsigned int color = doc["color"];
  String id = doc["id"];
  String effect = doc["effect"];
  int brightness = doc["brightness"];
  digitalWrite(LED_BUILTIN, HIGH);

  if (id_old!=id){
    id_old=id;
    Serial.println("entering1");
    if(effect=="std" or effect=="None"){
      strip.setBrightness(brightness);
      Serial.println("entering2");
      strip.fill(color);
      strip.show();
    }
    else if (effect == "rainbow"){
      strip.setBrightness(brightness);
      strip.show();
      rainbow(30);
      exit;
    }
    else if (effect == "fusion"){
      strip.setBrightness(brightness);
      strip.show();
      fusion(20);
      exit;
    }
  }
}


String callhttps() {
  //LED Blue
  digitalWrite(LED_BUILTIN, LOW);
  //Initialize object http
  HTTPClient http;
  //Connect host by https + fingerprint
  http.begin(host, "07:F5:09:A6:B2:F8:48:CE:DF:8E:AD:7C:A4:CC:D2:3F:12:06:DE:CB");

  //Get code, if normal then get data
  int httpCode = http.GET();
  if (httpCode > 0) {
    payload = http.getString();
    Serial.println("Got payload");
  } else {
    Serial.print("\n error");
    Serial.println(http.errorToString(httpCode).c_str());
  }
  //De-initialize object
  http.end();
  //Return payload
  return payload;
}

void connectWIFI() {
  //LED Blue
  digitalWrite(LED_BUILTIN, LOW);
  //Connect network
  WiFi.begin(ssid, pass);
  Serial.println("Connecting to ");
  Serial.print(ssid);
  strip.setBrightness(100);
  //Wait for connecting, the strip is blinking light-blue
  while (WiFi.status() != WL_CONNECTED) {
    strip.fill(0x1cccd9);
    strip.show();
    delay (1000);
    strip.fill(0x000000);
    strip.show();
    Serial.print(".");
    delay(1000);
  }

  //After connection LED Off
  Serial.print("\nCONNECTED ");
  Serial.println(ssid);
  digitalWrite(LED_BUILTIN, HIGH);
  return;
}

void rainbow(int wait) {
  // Hue of first pixel runs 5 complete loops through the color wheel.
  // Color wheel has a range of 65536 but it's OK if we roll over, so
  // just count from 0 to 5*65536. Adding 256 to firstPixelHue each time
  // means we'll make 5*65536/256 = 1280 passes through this outer loop:
  while (true){
  String datan;
  for (long firstPixelHue = 0; firstPixelHue < 65536; firstPixelHue += 256) {
      if(firstPixelHue%8192==0){
        datan=callhttps();
      }
      if (datan!=data){
        return;
      }
    for (int i = 0; i < strip.numPixels(); i++) { // For each pixel in strip...


      // Offset pixel hue by an amount to make one full revolution of the
      // color wheel (rge of 65536) along the length of the strip
      // (strip.numPixels() steps):an
      int pixelHue = firstPixelHue + (i * 65536L / strip.numPixels());
      // strip.ColorHSV() can take 1 or 3 arguments: a hue (0 to 65535) or
      // optionally add saturation and value (brightness) (each 0 to 255).
      // Here we're using just the single-argument hue variant. The result
      // is passed through strip.gamma32() to provide 'truer' colors
      // before assigning to each pixel:
      strip.setPixelColor(i, strip.gamma32(strip.ColorHSV(pixelHue)));
    }
    strip.show();
    delay(wait);
  }
  }
}

void fusion(int wait){
  while (true){
    String datan;
  for (int striphue=0; striphue < 65536; striphue += 64){
      if(striphue%8192==0){
        datan=callhttps();
      }
      if (datan!=data){
        return;
      }
    strip.fill(strip.gamma32(strip.ColorHSV(striphue)));
    strip.show();
    delay(wait);
  }
  }
}
