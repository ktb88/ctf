#include <unistd.h>
#include <iostream>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

using namespace std;

class memo
{
	public:
		char content[32];

		virtual void mWrite(char *input) {
			memcpy(content, input,32);
		}

		virtual void mRead() {
			puts(content);
		}
};

void getShell(){
	system("/bin/cat /home/free/flag");
}

int main(int argc, char **argv){
	setbuf(stdin, NULL);
	setbuf(stdout, NULL);

	int option;
	char *content;
	char name[4];
	memo *m;

	printf("%x\n", &name);
	read(0, name, 8);

	while(1){
		puts("input your content");
		content = (char*)malloc(32);
		read(0,content,31);
		content[31] = 0;

		puts("if you want to read your memo, press 1");
		read(0, &option, 8);
		if (option == 1)
			m->mRead();

		m = new memo;
		m->mWrite(content);
		delete m;
	}

	return 0;
}
