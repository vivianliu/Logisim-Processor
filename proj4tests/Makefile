SRCS1=$(wildcard *-test.circ)
TESTS=$(SRCS1:.circ=.txt)
SRCS2=$(wildcard *-limited.circ)
LIMIT=$(SRCS2:.circ=.txt)
SRCS3=$(wildcard *-basic.circ)
BASIC=$(SRCS3:.circ=.txt)
UNAME = $(shell uname)

# running on 200 SD machines
ifeq ($(UNAME),Darwin)
B1 := 75
B2 := 375
B3 := 574
B4 := 675
endif

# running on any other machines
ifneq ($(UNAME),Darwin)
B1 := 75
B2 := 225
B3 := 375
B4 := 465
endif

check: kill clean folder $(TESTS) process

limited: kill clean folder $(LIMIT) process

basic: kill clean folder $(BASIC) process

register: kill clean folder readwrite-reg.txt process

all: kill clean folder $(BASIC) $(LIMIT) $(TESTS) process

default: check

makeReadable: makeReadable.c
	gcc -o makeReadable makeReadable.c

%.std: %.circ makeReadable
	@echo "Creating readable output file..."
	@cat $*.out | ./makeReadable > youroutput/$@
	@sleep 1
	@echo "Done"

%.txt: %.circ %.std makeReadable
	@echo "Simulating: $<"
	@java -jar -Djava.awt.headless=true logisim-generic-2.7.1.jar -tty table $< | head -n `cat $*.out | wc -l` | ./makeReadable  | tee youroutput/$@ | diff -b - youroutput/$*.std | tee youroutput/$*.diff &

	@sleep 5
	@if [ `cat $*.out | wc -l` -le $(B1) ]; then \
		sleep 2; \
	elif [ `cat $*.out | wc -l` -le $(B2) ]; then \
		sleep 3; \
	elif [ `cat $*.out | wc -l` -le $(B3) ]; then \
		sleep 4; \
	elif [ `cat $*.out | wc -l` -le $(B4) ]; then \
		sleep 5; \
	else \
		sleep 6; \
	fi

	@echo "\t Test done. Killing process..."
	@ps -f -u `whoami` | grep java | grep -v grep | awk '{print $$2}' > process.txt
	@kill -9 `cat process.txt`
	@sleep 0.5
	@echo "\t Completed."

process:
	@echo ""
	@echo "Cleaning: process.txt"
	@rm -f process.txt
	@sleep 0.75
	@echo "<(-_-)>"
	@sleep 0.75
	@echo "<('_')>"
	@sleep 0.75
	@echo "<('_-<)"
	@sleep 0.75
	@echo "<(^_')>"
	@sleep 0.75
	@echo "(>'_')>"
	@sleep 0.75
	@echo "<(^_^)>"
	@sleep 0.75
	@echo "Completed."

clean: 
	@echo -n 'Clearing personal folder.'
	@sleep 0.5
	@echo -n '.'
	@sleep 0.5
	@echo -n '.'
	@sleep 0.5
	@rm -rf youroutput
	@echo "Completed."

folder:
	@echo -n 'Making personal folder.'
	@sleep 0.5
	@echo -n '.'
	@sleep 0.5
	@echo -n '.'
	@sleep 0.5
	@mkdir youroutput
	@echo "Completed."

kill:
	@ps -f -u `whoami` | grep java | grep -v grep | awk '{print $$2}' > process.txt
	@echo "Need to kill `cat process.txt | wc -l` processes"

	@while [[ `cat process.txt | wc -l` -gt 0 ]]; do \
		kill -9 `cat process.txt | head -1`; \
		sleep 1; \
		ps -f -u `whoami` | grep java | grep -v grep | awk '{print $$2}' > process.txt; \
		echo "`cat process.txt | wc -l` processes left"; \
	done
	@sleep 1
	@echo -n 'Processes killed. Ready to start testing.'
	@sleep 0.5
	@echo -n '.'
	@sleep 0.5
	@echo '.'
	@sleep 0.5
	@echo ""
