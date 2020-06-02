# ----------------------------------------------------------------- #
#  File   : Makefile
#  Author : peach
#  Date   : 8 July 2019
# ----------------------------------------------------------------- #

CC=g++

C_SRCS=cpp/main.cpp \
       cpp/lib/Comms.cpp \
       cpp/lib/Fader.cpp \
       cpp/lib/PlantSystems.cpp \
       ../../ArduinoMockout/src/Arduino.cpp

INCL=-I../../ArduinoMockout/src/ \
     -Icpp/lib/

OUT=app.run

all:
	$(CC) $(INCL) $(C_SRCS) -o $(OUT)
	@chmod +x $(OUT)
debug:
	$(CC) $(INCL) $(C_SRCS) -o $(OUT) -g
	@chmod +x $(OUT)
clean:
	@rm $(OUT)
