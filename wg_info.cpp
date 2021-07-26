#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>

void print_help(void){
	fprintf(stderr, "Usage:\n");
	fprintf(stderr, "    wg_info          -> run           `wg show wg0`\n");
	fprintf(stderr, "    wg_info up       -> run           `wg-quick up wg0`\n");
	fprintf(stderr, "    wg_info down     -> run           `wg-quick down wg0`\n");
	fprintf(stderr, "    wg_info transfer -> run and parse `wg show wg0 transfer`\n");
	return;
}

int main(const int argc, const char** argv)
{
	int _ret;

	_ret = setuid(geteuid());
	if(_ret != 0){
		fprintf(stderr, "Error setting the uid\n");
		exit(1);
	}

	if(argc == 1)
	{
		return system("wg show");
	}
	else if(argc == 2)
	{
		if(strcmp("transfer", argv[1]) == 0)
		{
			uint64_t rx, tx;
			FILE* fd = NULL;
			int ret;

			fd = popen("wg show wg0 transfer", "r");
			ret = fscanf(fd, "%*s\t%lu\t%lu", &rx, &tx);

			if(ret == 2)
			{
				printf("%lu\n%lu\n", rx, tx);
			}
			else
			{
				fprintf(stderr, "Could not parse the result\n");
				exit(1);
			}
			
			exit(pclose(fd));
		} 
		else if(strcmp("up", argv[1]) == 0)
		{
			return system("wg-quick up wg0");
		} 
		else if(strcmp("down", argv[1]) == 0)
		{
			return system("wg-quick down wg0");
		}
		else 
		{
			fprintf(stderr, "Invalid argument\n");
			print_help();
			return 1;
		}
	}
	else 
	{
		fprintf(stderr, "Invalid number of arguments\n");
		print_help();
		return 1;
	}
}
