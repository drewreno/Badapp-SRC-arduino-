#ifndef BAD_APPLE_H
#define BAD_APPLE_H

#include <ESP8266WiFi.h>
#include <WiFiClientSecure.h>
#include <ESP8266HTTPClient.h>
#include <Wire.h>
#include <SSD1306Wire.h>
#include <string>

#define SCREEN_WIDTH 128  // OLED display width, change according to your display
#define HEADER_SIZE 62
#define IMAGE_WIDTH 86
#define HEIGHT 64
#define FILE_SIZE 768
#define LINE_SIZE 12

SSD1306Wire display(0x3c, 12, 14);  // ADDRESS, SDA, SCL

WiFiClientSecure wifiClient;
HTTPClient http;

bool* img = new bool[IMAGE_WIDTH * HEIGHT];
unsigned char* buffer = new unsigned char[HEADER_SIZE];
unsigned char* data = new unsigned char[FILE_SIZE];

// Constants for frame handling
short frameNumber = 1; // Starting frame

#endif // BAD_APPLE_H
