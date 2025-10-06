#include "badapple.h"

void setup() {

  Serial.begin(115200);

  WiFi.begin("GWconnect", "");
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to WiFi");

  display.init();
  display.flipScreenVertically();
  wifiClient.setInsecure();

  memset(img, 0, sizeof(img));
  memset(data, 0, sizeof(data));

  String url = "https://raw.githubusercontent.com/drewreno/badappbmp/fullbmp";

  http.begin(wifiClient, url);
  delay(1000);
  Serial.println("starting");
  delay(1000);
}

void loop() { 
  Main();
  frameNumber += 3;
}

void Main() {
  memset(data, 0, sizeof(data));

  String url = "https://raw.githubusercontent.com/drewreno/badappbmp/fullbmp/frame_" + String(frameNumber) + ".bmp";

  http.begin(wifiClient, url);
  unsigned char httpCode = http.GET();

  if (httpCode == HTTP_CODE_OK) {
    WiFiClient *stream = http.getStreamPtr();
    
    /*Read BMP header
    unsigned char head[HEADER_SIZE];
    short w = head[18] + (((short)head[19]) << 8) + (((short)head[20]) << 16) + (((short)head[21]) << 24);
    short h = head[22] + (((short)head[23]) << 8) + (((short)head[24]) << 16) + (((short)head[25]) << 24);
    short lineSize = ((w + 31) / 32) * 4;
    short fileSize = lineSize * h;*/

    stream->readBytes(buffer, HEADER_SIZE);

    stream->readBytes(data, FILE_SIZE);

    for (unsigned char j = 0, rev_j = HEIGHT - 1; j < HEIGHT; j++, rev_j--) {
      for (unsigned char i = 0; i < IMAGE_WIDTH; i++) {
        unsigned char byte_ctr = i / 8;
        unsigned char data_byte = data[j * LINE_SIZE + byte_ctr];
        short pos = rev_j * IMAGE_WIDTH + i;
        unsigned char mask = 0x80 >> (i % 8);
        img[pos] = (data_byte & mask) ? 1 : 0;
      }
    }

    memset(data, 0, sizeof(data));

    //convert to xbm
    for (short y = 0; y < HEIGHT; y++) {
      for (short x = 0; x < IMAGE_WIDTH; x++) {
        short pos = y * IMAGE_WIDTH + x;
        short xbmPos = y * ((IMAGE_WIDTH + 7) / 8) + x / 8;

        if (img[pos] == 1) {
          data[xbmPos] |= (1 << (x % 8));
        } else {
          data[xbmPos] &= ~(1 << (x % 8));
        }
      }
    } 

    memset(img, 0, sizeof(img));

    //display
    display.clear();
    display.drawXbm(21, 0, IMAGE_WIDTH, HEIGHT, data);
    display.display();
    http.end();
  }
}

