#include <stdio.h>
#include <stdlib.h>
#define SIZE 512

// windows.h 미지원으로 인해 비트맵 파일 생성에 필요한 헤더파일 구축
typedef unsigned short WORD;
typedef unsigned long DWORD;
typedef unsigned long LONG;
typedef unsigned char BYTE;

#ifndef BI_RGB
#define BI_RGB 0
#endif

#pragma pack(1)
typedef struct tagBITMAPFILEHEADER {
    WORD bfType;
    DWORD bfSize;
    WORD bfReserved1;
    WORD bfReserved2;
    DWORD bfOffBits;
} BITMAPFILEHEADER;

typedef struct tagBITMAPINFOHEADER {
    DWORD biSize;
    LONG biWidth;
    LONG biHeight;
    WORD biPlanes;
    WORD biBitCount;
    DWORD biCompression;
    DWORD biSizeImage;
    LONG biXPelsPerMeter;
    LONG biYPelsPerMeter;
    DWORD biClrUsed;
    DWORD biClrImportant;
} BITMAPINFOHEADER;

struct RGBQUAD {
    unsigned char rgbBlue;
    unsigned char rgbGreen;
    unsigned char rgbRed;
    unsigned char rgbFlags;
};

struct RGBQUAD bmp_pal[256];

void main() {
    int i, j;
    unsigned char OrgImg[SIZE][SIZE];  // raw이미지를 저장하기 위한 배열
    unsigned char temp;                // raw이미지를 뒤집어서 저장하기위한 임시변수
    FILE *raw, *bmp, *fbalance;
    BITMAPFILEHEADER hf;
    BITMAPINFOHEADER hInfo;

    //파일헤드 정보입력
    hf.bfType = 0x4D42;  //"BM"이라는 값을 저장
    // Byte단위의 전체파일 크기
    hf.bfSize = (DWORD)(SIZE * SIZE + sizeof(BITMAPINFOHEADER) + sizeof(BITMAPFILEHEADER));
    hf.bfReserved1 = 0;  //예약된 변수
    hf.bfReserved2 = 0;  //예약된 변수
    //영상데이터 위치까지의 거리
    hf.bfOffBits = (DWORD)(sizeof(BITMAPINFOHEADER) + sizeof(BITMAPFILEHEADER));
    //영상헤드 정보입력
    hInfo.biSize = sizeof(BITMAPINFOHEADER);  //이 구조체의 크기
    hInfo.biWidth = SIZE;                     //픽셀단위로 영상의 폭
    hInfo.biHeight = SIZE;                    //영상의 높이
    hInfo.biPlanes = 1;                       //비트 플레인 수(항상 1)
    hInfo.biBitCount = 8;                     //픽셀당 비트수(컬러, 흑백 구별)
    hInfo.biCompression = BI_RGB;             //압축유무
    hInfo.biSizeImage = SIZE * SIZE;          //영상의 크기(Byte단위)
    hInfo.biXPelsPerMeter = 0;                //가로 해상도
    hInfo.biYPelsPerMeter = 0;                //세로 해상도
    // raw파일을 영상정보를 써준다
    // raw파일 읽기
    raw = fopen("HW02.raw", "rb");
    if (raw == NULL) {
        printf("File Open Error!\n");
        return;
    }
    fread(OrgImg, sizeof(char), SIZE * SIZE, raw);
    fclose(raw);

    // raw파일 뒤집어 주기
    for (i = 0; i < SIZE / 2; i++) {
        for (j = 0; j < SIZE; j++) {
            temp = OrgImg[i][j];
            OrgImg[i][j] = OrgImg[SIZE - i - 1][j];
            OrgImg[SIZE - i - 1][j] = temp;
        }
    }
    // 인포헤더 아래에 팔레트가 오므로 1024만큼 뒤에 비트맵 데이터 시작
    hf.bfOffBits += 1024;
    // 8비트 비트맵이므로 8로 수정
    hInfo.biBitCount = 8;

    // 팔레트 만들기
    for (int i = 0; i < 256; i++) {
        bmp_pal[i].rgbRed = (BYTE)(((i >> 5) & 0x07) * 255 / 7);
        bmp_pal[i].rgbGreen = (BYTE)(((i >> 2) & 0x07) * 255 / 7);
        bmp_pal[i].rgbBlue = (BYTE)(((i >> 0) & 0x03) * 255 / 3);
        bmp_pal[i].rgbFlags = 0;
    }

    // bmp파일로 저장
    bmp = fopen("hw1.bmp", "wb");
    fwrite(&hf, sizeof(char), sizeof(BITMAPFILEHEADER), bmp);
    fwrite(&hInfo, sizeof(char), sizeof(BITMAPINFOHEADER), bmp);
    fwrite(bmp_pal, sizeof(bmp_pal), 1, fbalance);
    fwrite(fbalance, sizeof(unsigned char), SIZE * SIZE, fbalance);
    fwrite(OrgImg, sizeof(char), hInfo.biSizeImage, bmp);
    fclose(bmp);
}