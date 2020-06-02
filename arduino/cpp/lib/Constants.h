/*
 **********************************************************************
 *  File   : Constants.h
 *  Author : peach
 *  Date   : 12 July 2019
 **********************************************************************
 */

#ifndef _CONSTANTS_H_
#define _CONSTANTS_H_

#define TRUE  1
#define FALSE 0

/*
 * WiFi Settings
 */
#define WIFI_SSID "__WIFI_NETWORK_NAME__"
#define WIFI_PWD  "__WIFI_NETWORK_PASSWORD__"

/*
 * Device IDs (for USB wiring)
 */
#define DEVICE_ID_FAN 0x01
#define DEVICE_ID_LED 0x02

/*
 * Pin Definitions and Levels for Arduino.
 */
#define PIN_FAN 5
#define PIN_LED_R 10
#define PIN_LED_G 9
#define PIN_LED_B 6
#define PIN_LIGHT_STRIP 6

/*
 * Pin Definitions and Levels for ATTiny85
 */
#ifdef ARDUINO_ARCH_AVR
#define PIN_LED_R 1
#define PIN_LED_G 3
#define PIN_LED_B 4
#endif

/*
 * I2C Addresses
 */
#define I2C_ADDRESS_CTRLR   0x00
#define I2C_ADDRESS_STRIP_1 0x01
#define I2C_ADDRESS_STRIP_2 0x02
#define I2C_ADDRESS_STRIP_3 0x03
#define I2C_ADDRESS_STRIP_4 0x04

/*
 * RF Pins - Nano
 */
#define PIN_RF_CE  7
#define PIN_RF_CSN 8

/*
 * RF Configuration
 */
#define RF_ADDRESS_BLUE           { 0xdc, 0x64, 0xb6, 0xe0, 0x01 }
#define RF_ADDRESS_GREEN          { 0xdc, 0x64, 0xb6, 0xe0, 0x02 }
#define RF_ADDRESS_RGB_BEDROOM    { 0xdc, 0x64, 0xb6, 0xe0, 0x03 }
#define RF_ADDRESS_RGB_DOORFRAME  { 0xdc, 0x64, 0xb6, 0xe0, 0x04 }
#define RF_ADDRESS_RGB_TENSEGRITY { 0xdc, 0x64, 0xb6, 0xe0, 0x05 }
#define RF_PAYLOAD_SIZE  32

#define RF_CMD_SET_RGBLEVEL 0x03
#endif // _CONSTANTS_H_
