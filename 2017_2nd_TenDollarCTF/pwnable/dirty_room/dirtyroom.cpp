#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

char name[32];

class Room
{
	public:
		Room() {}
		~Room(){}

		virtual void room_open() {}
		virtual void room_close() {}
};

class RoomA : public Room
{
	public:
		RoomA() {
			this->RoomNumber = 1;
			memset(this->RoomDesc, 0, 32);
		}
		~RoomA(){}

		int RoomNumber;
		char RoomDesc[32];
		void room_open() {
			printf("[RoomA] %d is opened \n", this->RoomNumber);
			this->set_room_name();
		}
		void room_close() {
			printf("[RoomA] %d is closed \n", this->RoomNumber);
		}
		void set_room_name(){
			int n_name = strlen(name);
			printf("[RoomA] set your room desc : ");
			read(0, this->RoomDesc + n_name, 32);
			printf("[RoomA] %s\n", this->RoomDesc);
		}
};

class RoomB : public Room
{
	public:
		RoomB(){
			this->RoomNumber = 2;
		}
		~RoomB(){}

		int RoomNumber;
		void room_open() {
			printf("[RoomB] %d is opened \n", this->RoomNumber);
		}
		void room_close() {
			printf("[RoomB] %d is closed \n", this->RoomNumber);
		}
};

RoomA *p_RoomA;
RoomB *p_RoomB;

void secret_function()
{
	FILE *fp;
	char buf[64] = {0,};

	fp = fopen("/home/dr/flag", "r");
	if (fp == NULL)
		exit(0);

	fgets(buf, 64, fp);
	printf("%s\n", buf);
	fclose(fp);
}

void set_name()
{
	printf("[*] set your name: ");
	read(0, name, 32);
	printf("Your name is : %s\n", name);
}

int main(int argc, char **argv)
{
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);

	int n;

	p_RoomA = new RoomA;
	p_RoomB = new RoomB;

	if (p_RoomA == NULL || p_RoomB == NULL)
		return -1;

	while(1) {
		printf("1) Open room A\n");
		printf("2) Close room A\n");
		printf("3) Open room B\n");
		printf("4) Close room B\n");
		printf("5) Exit room \n");

		scanf("%d%*c", &n);

		switch( n ) {
			case 1: {
				p_RoomA->room_open();
			} break;
			case 2: {
				p_RoomA->room_close();
			} break;
			case 3: {
				p_RoomB->room_open();
			} break;
			case 4: {
				p_RoomB->room_close();
			} break;
			case 5: {
				return 0;
			} break;
			case 31337: {
				set_name();
			} break;
			default : {
				printf("Wrong ! \n");
			} break;
		}
	}

	return 0;
}
