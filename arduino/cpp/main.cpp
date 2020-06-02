/*
 **********************************************************************
 *  File   : main.cpp
 *  Author : peach
 *  Date   : 9 July 2019
 **********************************************************************
 */
#include <stdio.h>
#include <iostream>

#include "Arduino.h"
#include "Fader.h"
#include "Comms.h"

int main() {
    setupSerial();
    byte command[COMMAND_ARRAY_SIZE];
    int deviceId = 0;
    int commandSize = 0;

    Serial.push(0x06);
    Serial.push(0x05);
    Serial.push(0x01);
    Serial.push(0x10);
    Serial.push(0xFF);
    Serial.push(0xA0);

    getCommand(deviceId, commandSize, command);

    std::cout << "Device id is " << deviceId << std::endl;
    std::cout << "Command Size is " << commandSize << std::endl;
    std::cout << "Command is " << command[0] << command[1] << command[2]
            << command[3] << "-----" << std::endl;

    return 1;
}

