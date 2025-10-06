#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define IMAGE_WIDTH 86
#define IMAGE_HEIGHT 64
#define BMP_HEADER_SIZE 62

// Function to calculate the padding for BMP rows
int bmpRowPadding() {
    return (4 - ((IMAGE_WIDTH + 7) / 8) % 4) % 4;
}

void printBinaryData(const char *bmpPath) {
    FILE *bmpFile = fopen(bmpPath, "rb");

    if (!bmpFile) {
        perror("File opening failed");
        return;
    }

    // Skip BMP header
    fseek(bmpFile, BMP_HEADER_SIZE, SEEK_SET);

    // Calculate padding
    int padding = bmpRowPadding();
    printf("Row padding: %d bytes\n", padding);

    int rowWidthBytes = (IMAGE_WIDTH + 7) / 8; // Bytes per row
    unsigned char buffer[rowWidthBytes];
    for (int row = 0; row < IMAGE_HEIGHT; ++row) {
        if (fread(buffer, 1, rowWidthBytes, bmpFile) != rowWidthBytes) {
            perror("Failed to read BMP data");
            fclose(bmpFile);
            return;
        }
        
        for (int col = 0; col < IMAGE_WIDTH; ++col) {
            int byteIndex = col / 8;
            int bitIndex = 7 - (col % 8);
            unsigned char pixelByte = buffer[byteIndex];
            int pixel = (pixelByte >> bitIndex) & 1;
            printf("%d", pixel);
        }

        // Skip BMP padding
        fseek(bmpFile, padding, SEEK_CUR);
        printf("\n"); // New line after each row for clarity
    }

    fclose(bmpFile);
}

int main() {
    const char *bmpPath = "frame_1000.bmp";

    printBinaryData(bmpPath);

    return 0;
}