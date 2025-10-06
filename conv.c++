#include <iostream>
#include <vector>
#include <ESP8266WiFi.h>

class BMPReader {
public:
    static std::vector<unsigned char> read_bmp(WiFiClient& stream) {
        std::vector<unsigned char> header(54);

        // Read BMP header from the stream
        stream.readBytes(reinterpret_cast<char*>(header.data()), header.size());

        int w = header[18] + (static_cast<int>(header[19]) << 8) + (static_cast<int>(header[20]) << 16) + (static_cast<int>(header[21]) << 24);
        int h = header[22] + (static_cast<int>(header[23]) << 8) + (static_cast<int>(header[24]) << 16) + (static_cast<int>(header[25]) << 24);

        // Lines are aligned on 4-byte boundary
        int lineSize = (w / 8 + (w / 8) % 4);
        int fileSize = lineSize * h;

        std::vector<unsigned char> img(w * h);
        std::vector<unsigned char> data(fileSize);

        // Read data from the stream
        stream.readBytes(reinterpret_cast<char*>(data.data()), fileSize);

        // Decode bits
        for (int j = 0, rev_j = h - 1; j < h; j++, rev_j--) {
            for (int i = 0; i < w; i++) {
                int byteCtr = i / 8;
                unsigned char dataByte = data[j * lineSize + byteCtr];
                int pos = rev_j * w + i;
                unsigned char mask = 0x80 >> (i % 8);
                img[pos] = (dataByte & mask) ? 1 : 0;
            }
        }

        return img;
    }
};
