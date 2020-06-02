/*
 **********************************************************************
 *  File   : PlantSystems.h
 *  Author : peach
 *  Date   : 15 July 2019
 **********************************************************************
 */

#ifndef _PLANT_SYSTEMS_H_
#define _PLANT_SYSTEMS_H_

/**
 * PlantSystem - The base class for the plants.
 */
class PlantSystem {
protected:
    // Whether or not system is turned on.
    bool _isEnabled;
    int _pin;
public:
    virtual bool isEnabled() = 0;
    virtual void enable() = 0;
    virtual void disable() = 0;
};

/**
 * Fan and Light have identical signatures.
 */
class Fan: public PlantSystem {
public:
    Fan(int pin);
    bool isEnabled();
    void enable();
    void disable();
};

class LedLight: public PlantSystem {
protected:
    int _power;
public:
    LedLight(int pin);
    bool isEnabled();
    void enable();
    void disable();

    // Power is an integer between 0 and 255.
    // It's decoupled from the enabled/disabled state.
    void setPower(int power);
    int getPower();
};

#endif // _PLANT_SYSTEMS_H_
