/*
 **********************************************************************
 *  File   : Comms.h
 *  Author : peach
 *  Date   : 15 July 2019
 **********************************************************************
 */

#ifndef _COMMS_H_
#define _COMMS_H_

#include "Arduino.h"

#define INSTRUCTION_ARRAY_SIZE 20
#define COMMAND_ARRAY_SIZE 16

void getCommand(int &deviceId, int &commandSize, byte command[]);
void setupSerial();

#endif // _COMMS_H_
