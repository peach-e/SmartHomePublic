/*
 **********************************************************************
 *  File   : RequestHandler.cpp
 *  Author : peach
 *  Date   : 5 May 2020
 **********************************************************************
 */


#ifndef ARDUINO_ARCH_AVR // TODO: Make this be ifdef ARCH 8266 whatever.

#include "RequestHandler.h"
#include <ESP8266WebServer.h>
#include <Wire.h>

#define URI_KEYWORD "/strip/"
#define URI_KEWYORD_LENGTH 7

int RGBRequestHandler::_parseRGBValue(const String& jsonString, char letter) {
    // Pull off curly brackets.
    // String goes from   {"r":123,"g":456,"b":789}
    //               to   "r":123,"g":456,"b":789
    String workingStr = jsonString.substring(1, jsonString.length() - 1);

    // Find where the letter is and make sure it's present in string.
    int index;
    index = workingStr.indexOf(letter);
    if (index < 0) {
        return 0;
    }

    // Strip of the letter we want as well as the <<":>> afterward
    // workingStr should look like     123,"g":456,"b":789
    //                          or             456,"b":789
    //                          or                     789
    workingStr = workingStr.substring(index + 3);

    // Look for the index of the comma after the number.
    // If there isn't one, just to go end of string.
    index = workingStr.indexOf(',');

    int result = 0;
    if (index > 0) {
        // Strip out the 123 or 456 that ends before the comma.
        result = workingStr.substring(0, index).toInt();
    } else {
        // The 789 doesn't have a comma, so just go to end of string.
        result = workingStr.toInt();
    }

    // If an integer wasn't successfully parsed, should get 0 as result.
    return result;
}

void RGBRequestHandler::_sendRgbValues(int address, char r, char g, char b) {
    Wire.beginTransmission(address);
    Wire.write(r);
    Wire.write(g);
    Wire.write(b);
    Wire.write(0x00);
    Wire.endTransmission();
}

bool RGBRequestHandler::canHandle(HTTPMethod method, String uri) {
    return uri.startsWith(URI_KEYWORD);
}

bool RGBRequestHandler::handle(ESP8266WebServer& server,
                               HTTPMethod requestMethod, String requestUri) {
    // Remove the /strip/ from the URI, leaving just the integer.
    requestUri.remove(0, URI_KEWYORD_LENGTH);
    int strip = requestUri.toInt();

    // Parse the POST request payload.
    String jsonString = server.arg("plain");
    char r = _parseRGBValue(jsonString, 'r');
    char g = _parseRGBValue(jsonString, 'g');
    char b = _parseRGBValue(jsonString, 'b');
    _sendRgbValues(strip, r, g, b);

    server.send(200, "text/plain", "Updated strip successfully.");
    return true;
}

void RGBRequestHandler::setup() {
    Wire.begin();
}

#endif