#include <bitmap.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define ROW 512             // VER = 512
#define COL 512             // HOR = 512
#define F_SIZE (ROW * COL)  // F_SIZE = 512*512
#define WIDTHBYTES(bits) (((bits) + 31) / 32 * 4)

unsigned char ResultImage[512][512] = {0};

int Gray_Raw2Bmp(char *pRawName, DWORD nWidth, DWORD nHeight, char *pBmpName) {
    BITMAPFILEHEADER file_h;
    BITMAPINFOHEADER info_h;
    DWORD dwBmpSize = 0;
    DWORD dwRawSize = 0;
    DWORD dwLine = 0;
    long lCount, i;
    FILE *in, *out;
    char *pData = NULL;
    RGBQUAD rgbPal[256];

    in = fopen(pRawName, "rb");
    if (in == NULL) {
        printf("File Open Error!\n");
        return 0;
    }

    out = fopen(pBmpName, "wb");

    file_h.bfType = 0x4D42;
    file_h.bfReserved1 = 0;
    file_h.bfReserved2 = 0;
    file_h.bfOffBits = sizeof(rgbPal) + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);
    info_h.biSize = sizeof(BITMAPINFOHEADER);
    info_h.biWidth = (DWORD)nWidth;
    info_h.biHeight = (DWORD)nHeight;
    info_h.biPlanes = 1;
    info_h.biBitCount = 8;
    info_h.biCompression = BI_RGB;
    info_h.biXPelsPerMeter = 0;
    info_h.biYPelsPerMeter = 0;
    info_h.biClrUsed = 0;
    info_h.biClrImportant = 0;

    dwLine = ((((info_h.biWidth * info_h.biBitCount) + 31) & ~31) >> 3);
    dwBmpSize = dwLine * info_h.biHeight;
    info_h.biSizeImage = dwBmpSize;
    file_h.bfSize = dwBmpSize + file_h.bfOffBits + 2;

    dwRawSize = info_h.biWidth * info_h.biHeight;
    pData = (char *)malloc(sizeof(char) * dwRawSize + 16);

    if (pData) {
        fread(pData, 1, dwRawSize, in);

        for (i = 0; i < 256; i++) {
            rgbPal[i].rgbRed = (BYTE)(i % 256);
            rgbPal[i].rgbGreen = rgbPal[i].rgbRed;
            rgbPal[i].rgbBlue = rgbPal[i].rgbRed;
            rgbPal[i].rgbReserved = 0;
        }

        fwrite((char *)&file_h, 1, sizeof(BITMAPFILEHEADER), out);
        fwrite((char *)&info_h, 1, sizeof(BITMAPINFOHEADER), out);
        fwrite((char *)rgbPal, 1, sizeof(rgbPal), out);
        lCount = dwRawSize;

        for (lCount -= (long)info_h.biWidth; lCount >= 0; lCount -= (long)info_h.biWidth) {
            fwrite((pData + lCount), 1, (long)dwLine, out);
        }

        free(pData);
    }

    fclose(in);
    fclose(out);

    return 1;
}

int main() {
    int i, j;
    FILE *fout;

    // 밝기증가
    for (i = 0; i < COL; i++) {
        for (j = 0; j < 100; j++) {
            ResultImage[i][j] = 120;
        }

        for (j = 100; j < 200; j++) {
            ResultImage[i][j] = (char)(j * (0.15) + 105);
        }

        for (j = 200; j < 280; j++) {
            ResultImage[i][j] = (char)(j * (90 / 80) - 90);
        }

        for (j = 280; j < 300; j++) {
            ResultImage[i][j] = (char)(j * 0.75 + 15);
        }

        for (j = 300; j < ROW; j++) {
            ResultImage[i][j] = 240;
        }
    }

    fout = fopen("HW01.raw", "wb");
    fwrite(ResultImage, sizeof(char), F_SIZE, fout);
    fclose(fout);

    return 0;
}