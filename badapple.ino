#include "badapple.h"
#include <Arduino.h>
#include <string>

SSD1306Wire display(0x3c, 12, 14);  // ADDRESS, SDA, SCL

void setup() {
  Serial.begin(115200);
  setupWiFi(); // Connect to WiFi
  display.init();
  display.flipScreenVertically();
}

void loop() { 
  fetchAndDisplayFrame();
  delay(FrameINT);
}

void storeInArray(uint8_t byte) {
    if (currentIndex < SIZE) {
        outputArray[currentIndex++] = byte;
    }
}


void fetchAndDisplayFrame() {
  Serial.println("start fetch");

  WiFiClientSecure wifiClient;  // Declare the WiFiClientSecure object
  wifiClient.setInsecure(); // Bypass SSL certificate verification

  // Update this URL with your actual GitHub repository path
  String url = "https://raw.githubusercontent.com/drewreno/badapp/main/frame_" + String(frameNumber) + ".xbm";

  HTTPClient http;
  http.begin(wifiClient, url);
  int httpCode = http.GET();

  if (httpCode > 0) {
    WiFiClient *stream = http.getStreamPtr();

    // Reading the entire content of the file into a String object.
    payload = stream->readString();

    Serial.println("Downloaded frame " + String(frameNumber));
  } else {
    // Handle the case where the HTTP GET request failed
    Serial.println("Error in HTTP request");
    payload = "";  // Return an empty string to indicate failure
  }

  http.end(); // Close the connection

  // Convert the payload String to a const char* and pass it to getImageBits
  const char* payloadChar = payload.c_str();
  currentIndex = 0; // Reset the index before filling the array
  getImageBits(payloadChar, storeInArray); // Process data and store in outputArray

  displayFrame();
  frameNumber = frameNumber + 5;
}

void getImageBits(const char* data, void (*callback)(uint8_t)) {
    // Find the start and end of the array in the character buffer
    const char* start = strchr(data, '{') + 1;
    const char* end = strchr(start, '}');
    
    // Process the elements in the array
    while (start < end) {
        // Find the next comma and convert the hexadecimal value
        const char* comma = strchr(start, ',');
        if (comma == nullptr) {
            comma = end;  // Last element
        }
        
        // Calculate the length of the element
        size_t elementLength = comma - start;

        // Convert the hexadecimal string to a uint8_t and pass it to the callback
        char element[3];  // Assuming each element is two hex characters and null-terminated
        strncpy(element, start, elementLength);
        element[elementLength] = '\0';

        uint8_t byteValue = strtoul(element, NULL, 16);
        callback(byteValue);

        // Move to the next element
        start = comma + 1;
    }
}

void displayFrame() {

  // Draw the XBM image
  display.clear();
  display.drawXbm((display.getWidth() - image_width) / 2, 
                  (display.getHeight() - image_height) / 2, image_width, image_height, outputArray);
  display.display();

  for (int i = 0; i < sizeof(outputArray); i++) {
  }
  Serial.println("display call");
}
