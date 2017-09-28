#include <stdio.h>
#include <string.h>
#include <unistd.h>

char *credential = "***************************";

void secret_action()
{
	system("/bin/cat /home/login/flag");
}

void init()
{
	setvbuf(stdin, 0, 2, 0);
	setvbuf(stdout, 0, 2, 0);
	alarm(60);
}

int login(char *pw)
{
	if (strncmp(credential, pw, strlen(credential)) == 0)
		return 1;
	return 0;
}

int admin_action()
{
	char cmd[1024] = {0,};
	unsigned char size;
	unsigned char index;
	printf("[*] Hello, admin \n");
	printf("Give me your command : ");
	read(0, cmd, 1023);

	size = strlen(cmd) + 1;

	for (index=0 ; index < size ; index++) {
		if (cmd[index] < 'a' || cmd[index] > 'z') {
			printf("[*] for secure commands, only lower cases are expected. Sorry admin\n");
			return 0;
		}
	}

	printf(cmd);
	return 0;
}

int main(int argc, char **argv, char **env)
{
	init();

	char buf_pw[32] = {0,};
	int idx = 0;

	printf("[*] Welcome admin login system! \n\n");
	printf("Login with your credential...\n");
	printf("Credential : ");

	read(0, buf_pw, 512);

	if ( login(buf_pw) == 0) {
		printf("[!] Sorry, wrong credential\n");
		return 0;
	}

	while ("RUN") {
		printf("0) exit\n");
		printf("1) admin action\n");

		scanf("%d", &idx);

		if (idx == 0) {
			printf("Good bye, admin :)\n");
			return 0;
		} else if (idx != 1) {
			printf("Wrong.\n");
			continue;
		}

		admin_action();
	}
	return 0;
}
