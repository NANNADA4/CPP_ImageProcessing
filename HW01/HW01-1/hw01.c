#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define ROW 512             // 열 해상도 512
#define COL 512             // 행 해상도 512
#define F_SIZE (ROW * COL)  // 해상도 512 x 512

unsigned char Image[512][512];  // 이미지를 불러오기위해 배열 선언

int main() {
    int i, j;
    FILE *fpin, *fpout;

    // 파일을 바이너리로 불러오기
    fpin = fopen("lena_raw_512x512.raw", "rb");
    fread(Image, sizeof(char), F_SIZE, fpin);
    fclose(fpin);

    // 밝기증가
    for (i = 0; i < COL; i++) {
        // 0~100까지 밝기값 120
        for (j = 0; j < 100; j++) {
            Image[i][j] = 120;
        }

        // 100~200까지 밝기값 120~135
        for (j = 100; j < 200; j++) {
            Image[i][j] = (char)(j * (0.15) + 105);
        }

        // 200~280까지 밝기값 135~225
        for (j = 200; j < 280; j++) {
            Image[i][j] = (char)(j * (90 / 80) - 90);
        }

        // 280~300까지 밝기값 225~240
        for (j = 280; j < 300; j++) {
            Image[i][j] = (char)(j * 0.75 + 15);
        }

        // 300~512까지 밝기값 240
        for (j = 300; j < ROW; j++) {
            Image[i][j] = 240;
        }
    }

    fpout = fopen("HW01.raw", "wb");
    fwrite(Image, sizeof(char), F_SIZE, fpout);
    fclose(fpout);

    return 0;
}