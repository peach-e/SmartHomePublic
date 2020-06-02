/*
 **********************************************************************
 *  File   : SoftwarePWM.h
 *  Author : peach
 *  Date   : 4 May 2020
 **********************************************************************
 */

#ifndef _SOFTWARE_PWM_H_
#define _SOFTWARE_PWM_H_

class DigitalPWM {
private:
    int _pin;
    int _dutyCycle;
    int _count;
public:
    /*
     * Sets specified pin to digital output with current class.
     */
    DigitalPWM(int pin);

    /*
     * Reset pin on destruction.
     */
    ~DigitalPWM();

    /*
     * Set duty cycle to a number between 0 and 255.
     * 255 is full on, 0 is full off.
     *
     * NOTE: Due to hardware limitations in the implementation, this 255 might get aliased
     * if we can only use the most significant few bits.
     */
    void setPower(unsigned char power);

    /*
     * Get current power setting.
     */
    int getPower();

    /*
     * Call this function very often to cause the light to blink on and off at
     * approximately the duty cycle specified by Power.
     */
    void step();
};

#endif // _SOFTWARE_PWM_H_