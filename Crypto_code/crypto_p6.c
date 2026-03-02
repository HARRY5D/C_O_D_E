#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

/* Simple pseudo AES key generator */
void generate_aes_key(unsigned char *key, int len) {
    for(int i=0;i<len;i++)
        key[i] = rand()%256;
}

/* Fake RSA encryption (demo only) */
void rsa_encrypt(unsigned char *key, int len) {
    for(int i=0;i<len;i++)
        key[i] ^= 0xAA;   // simple reversible operation
}

void rsa_decrypt(unsigned char *key, int len) {
    for(int i=0;i<len;i++)
        key[i] ^= 0xAA;
}

int main() {

    srand(time(NULL));

    unsigned char aes_key[32];
    generate_aes_key(aes_key,32);

    printf("Generated AES-256 Key:\n");
    for(int i=0;i<32;i++) printf("%02X",aes_key[i]);
    printf("\n");

    unsigned char encrypted_key[32];
    memcpy(encrypted_key,aes_key,32);

    rsa_encrypt(encrypted_key,32);

    printf("\nEncrypted AES Key (via RSA simulation):\n");
    for(int i=0;i<32;i++) printf("%02X",encrypted_key[i]);
    printf("\n");

    rsa_decrypt(encrypted_key,32);

    printf("\nDecrypted AES Key at Receiver:\n");
    for(int i=0;i<32;i++) printf("%02X",encrypted_key[i]);
    printf("\n");

    return 0;
}

/*
hjdd
*/