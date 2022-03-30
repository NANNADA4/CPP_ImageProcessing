#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define ROW 512             // VER = 512
#define COL 512             // HOR = 512
#define F_SIZE (ROW * COL)  // F_SIZE = 512*512

unsigned char ResultImage[512][512] = {0};

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