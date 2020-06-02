/*
 **********************************************************************
 *  File   : Fader.h
 *  Author : peach
 *  Date   : 15 July 2019
 **********************************************************************
 */

#ifndef _FADER_H_
#define _FADER_H_

// Arbitrary, but should be 2 or more to support 2 LEDs fading at same time.
#define N_FADE_JOBS 20

// Adds a fade job to the queue and returns
// number of fade jobs you have on the go.
int addFadeJob(int initialValue, int finalValue, int numberSteps,
               void (*callback)(int));

/*
 * Steps all fade jobs and cleans up the completed ones.
 */
void fade();

/*
 * Return number of fade jobs.
 */
int getNumFadeJobs();

/*
 * Fades all jobs and returns number of remaining jobs.
 */
int fade_DEPRECATED();

// Class for the actual fade jobs, which get created, run, and destroyed.
class FadeJob {
private:
    int _initialValue;
    int _finalValue;
    int _currentStep;
    int _numberSteps;
    void (*_callback)(int);
public:
    FadeJob(int, int, int, void (*)(int));
    int stepFade();
};

#endif /* _FADER_H_ */
