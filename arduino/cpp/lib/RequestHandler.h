/*
 **********************************************************************
 *  File   : RequestHandler.h
 *  Author : peach
 *  Date   : 5 May 2020
 **********************************************************************
 */
#ifndef _REQUESTHANDLER_H
#define _REQUESTHANDLER_H

#include <ESP8266WebServer.h>

/*
 * Custom request handler so that we can parse URI for parameters and deal with
 * JSON parameters.
 */
class RGBRequestHandler : public RequestHandler {
private:
    /*
     * Pass in a JSON string that looks like {"r":10,"g":17,"b":5}, and a
     * character like 'g', and we'll be able to figure out that you want 17 as a
     * result.
     */
    int _parseRGBValue(const String& jsonString, char letter);

    /*
     * Send RGB values down the I2C bus.
     */
    void _sendRgbValues(int address, char r, char g, char b);

public:
    /*
     * Check that URI looks like http://192.168.0.45/LED/7
     */

    bool canHandle(HTTPMethod method, String uri);

    /*
     * Handle a valid request.
     */
    bool handle(ESP8266WebServer& server, HTTPMethod requestMethod,
                String requestUri);

    /*
     * Call before starting server.
     */
    void setup();
};

#endif // _REQUESTHANDLER_H