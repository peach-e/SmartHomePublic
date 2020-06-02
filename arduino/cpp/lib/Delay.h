/*
 **********************************************************************
 *  File   : Delay.h
 *  Author : peach
 *  Date   : 4 May 2020
 **********************************************************************
 */

#ifndef _DELAY_H_
#define _DELAY_H_

class NonBlockingDelay {
private:
    long int _initialTime;
    long int _targetTime;
    int _countdownTime;
public:
    /*
     * Creates and starts a non-blocking timer for the specified length.
     */
    NonBlockingDelay(int milliseconds);

    /*
     * Returns true if the countdown time since last reset has expired.
     */
    bool isExpired();

    /*
     * Resets Timer to last used countdown or to new countdown.
     */
    void reset();
    void reset(int milliseconds);
};

#endif // _DELAY_H_