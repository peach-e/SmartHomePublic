/*
 **********************************************************************
 *  File   : Comms.cpp
 *  Author : peach
 *  Date   : 28 Feb 2019
 **********************************************************************
 */

#ifndef ARDUINO_ARCH_AVR

#include "Arduino.h"
#include "Comms.h"
#include "Constants.h"

#define BAUD_RATE 9600

byte instructionArray[INSTRUCTION_ARRAY_SIZE];

void getCommand(int &deviceId, int &commandSize, byte command[]) {
    bool receivingCommand = TRUE;
    int instructionSize = 0;
    int bytesReceived = 0;

    // Keep peeling bytes off Serial until we've gathered the
    // number which the first byte tells us to expect.
    //
    // If you get stuck in a state where you're expecting more bytes,
    // the state can be reset by sending in a whole bunch
    // (e.g. INSTRUCTION_ARRAY_SIZE) of 0x00s.
    while (receivingCommand) {
        // Get a byte when it becomes available.
        if (Serial.available()) {
            instructionArray[bytesReceived] = Serial.read();
            bytesReceived++;

            // The first byte we get tells us the total size.
            if (bytesReceived == 1) {
                instructionSize = instructionArray[0];
                // If the size of instruction is zero, reset.
                if (instructionSize == 0) {
                    bytesReceived = 0;
                    continue;
                }
            }

            // If we have received as many as we're expecting, turn off the receiver.
            if (bytesReceived == instructionSize && bytesReceived > 0) {
                receivingCommand = FALSE;
            }
        }
    }

    deviceId = instructionArray[1];
    commandSize = instructionSize - 2;
    for (int i = 0; i < commandSize; i++) {
        // i is index of instruction array where command is found.
        command[i] = instructionArray[i + 2];
    }

    return;
}

void setupSerial() {
    Serial.begin(BAUD_RATE);
}

#endif