/*******************************
   File:   crpd_server.ino
   Author: peach
   Date:   4 May 2020
 *******************************/
#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include "Constants.h"
#include "RequestHandler.h"

ESP8266WebServer server(80);
RGBRequestHandler requestHandler;

void handleRoot();
void handleNotFound();

void setup() {
  // Initialize request handler.
  requestHandler.setup();

  // Start Serial.
  Serial.begin(115200);
  delay(10);
  Serial.println('\n');

  // Connect to Wifi.
  Serial.println("Connecting ...");
  WiFi.begin(WIFI_SSID, WIFI_PWD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(250);
    Serial.print('.');
  }
  Serial.println('\n');
  Serial.print("Connected to ");
  Serial.println(WiFi.SSID());
  Serial.print("IP address:\t");
  Serial.println(WiFi.localIP());

  // Turn on the lights because they look cool
  // and we know WiFi works.
  pinMode(2, OUTPUT);
  digitalWrite(2, LOW);

  // Setup Server.
  server.on("/", HTTP_GET, handleRoot);
  server.addHandler(&requestHandler);
  server.onNotFound(handleNotFound);

  server.begin();
  Serial.println("HTTP server started");
}

void loop(void) {
  server.handleClient();
}

void handleRoot() {
  server.send(200, "text/html", "Please use prescribed HTTP interface to talk to server.");
}

void handleNotFound() {
  server.send(404, "text/plain", "404: Not found");
}
