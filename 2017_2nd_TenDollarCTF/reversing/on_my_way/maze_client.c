#include <sys/socket.h>
#include <sys/types.h>
#include <arpa/inet.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <openssl/md5.h>

int encrypt(char *p_recv, char *p_send, char ch, unsigned int rnd_seed) {
	MD5_CTX context;

	char digest[16];
	char temp[256];
	unsigned int *ptr;
	char md5string[33];

	memset(temp, 0, 256);
	sprintf(temp, "%c%u", ch, rnd_seed);

	MD5_Init(&context);
	MD5_Update(&context, temp, strlen(temp));
	MD5_Final(digest, &context);

	memset(md5string, 0, 33);
	for(int i=0 ; i<16 ; i++)
		sprintf(&md5string[i*2], "%02x", (unsigned char)digest[i]);
	memcpy(p_send, md5string, 0x20);

	for(int i=1 ; i<4 ; i++)
	{
		memset(temp, 0, 256);
		memset(md5string, 0, 33);

		ptr = (unsigned int *)(p_recv + 4 * i);
		sprintf(temp, "%u%u", *ptr, rnd_seed);

		MD5_Init(&context);
		MD5_Update(&context, temp, strlen(temp));
		MD5_Final(digest, &context);

		for(int i=0 ; i<16 ; i++)
			sprintf(&md5string[i*2], "%02x", (unsigned char)digest[i]);
		memcpy(p_send+(0x20*i), md5string, (0x20*i));
	}
	p_send[strlen(p_send)] = '\n';
	p_send[strlen(p_send)] = 0;
	return 0;
}

int main(int argc, char **argv)
{
	if (argc != 2) {
		printf("[USAGE] %s [SERVER IP]\n", argv[0]);
		return 0;
	}

	srand(31337);
	unsigned int rnd_seed = 0;
	int i, n;

	for (i=0 ; i<31337; i++)
		rnd_seed ^= rand();

	int sockfd = 0;
	struct sockaddr_in serv_addr;
	char recvBuf[1024];
	char sendBuf[1024];

    if((sockfd = socket(AF_INET, SOCK_STREAM, 0)) < 0)
    {
        printf("[*] Fail to create socket\n");
        return 1;
    }

	memset(&serv_addr, 0, sizeof(serv_addr));

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(31337);

    if(inet_pton(AF_INET, argv[1], &serv_addr.sin_addr)<=0)
    {
		printf("[*] Fail to get inet_pton\n");
        return 1;
    }

    if( connect(sockfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0)
    {
		printf("[*] Fail to connect the server \n");
       	return 1;
    }

    while ("RUN")
    {
		memset(recvBuf, 0, 1024);
		n = read(sockfd, recvBuf, sizeof(recvBuf)-1);
        recvBuf[n] = 0;

        if (n < 0) {
            printf("[*] recv error \n");
            return 1;
        }

		unsigned int offset = 0;
		unsigned int *p = recvBuf;
		char ch;

		if (*p == 0xdeadface)
			offset = 0x10;

		printf("%s\n", recvBuf + offset);

		if (*p == 0xdeadface) {
			do {
				ch = getchar();
				fflush(stdin);
			} while (ch != 'U' && ch != 'D' && ch != 'R' && ch != 'L' && ch != 'Q');
			memset(sendBuf, 0, 1024);
			encrypt(recvBuf, sendBuf, ch, rnd_seed);
			write(sockfd, sendBuf, strlen(sendBuf));
		}
    }

	return 0;
}



