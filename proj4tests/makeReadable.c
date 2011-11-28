#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 1) {
        printf("Usage: %s\n", argv[0]);
        return 2;
    }

    /* we're not going to worry about long lines */
    char buffer[400000];

    while (!feof(stdin) && !ferror(stdin)) {
        if (!fgets(buffer, sizeof(buffer), stdin)) {
            break;
        }
	char *buf = buffer;
	int counter = 0;
	while (*(buf-1) != '\n') {
	    unsigned int thisNum = 0;
	    char thisNumStr[500];
	    char *ptr = thisNumStr;
	    while (*buf != '\t' && *buf != '\n') { // tab or carriage return
		if ('0' == *buf) {
		    thisNum = thisNum << 1;
		} else if ('1' == *buf) {
		    thisNum = (thisNum << 1) | 1;
		}
		if (*buf != 13) {
		    *(ptr++) = *(buf++);
		} else {
		    buf++; // Skip carraige return
		}
	    }
	    buf++; // Skip the tab
	    *ptr = '\0';
	    switch (counter++) {
	    case 0:
	    case 1:
	    case 2:
	    case 3: printf("$r%d value:\t\t", counter);
		break;
	    case 4:
	    case 5: printf("Display %d value:\t", counter - 4);
		break;
	    case 6: printf("Clk Count:\t\t");
		break;
	    case 7: printf("Mem Data:\t\t");
		break;
	    case 8: printf("Mem Address:\t\t");
		break;
	    case 9: printf("Write Enabled:\t\t");
		break;
	    default: printf("Error - Counter is too high - too many columns in input\n");
		return 0;
	    }
	    printf("0b%s\t%d\t0x%x\n", thisNumStr, thisNum, thisNum);
	}
	printf("\n");
    }

    if (ferror(stdin)) {
        perror(argv[0]);
        return 1;
    }

    return 0;
}

