/*
 **********************************************************************
 *  File   : Fader.cpp
 *  Author : peach
 *  Date   : 15 July 2019
 **********************************************************************
 */

#include "Arduino.h"
#include "Fader.h"

// The job queue.
FadeJob* _fadeJobs[N_FADE_JOBS];
int _numFadeJobs = 0;

int addFadeJob(int initialValue, int finalValue, int numberSteps,
               void (*callback)(int)) {

    // Create the fade job and add it to our queue.
    _fadeJobs[_numFadeJobs] = new FadeJob(initialValue, finalValue, numberSteps,
                                          callback);
    _numFadeJobs++;

    // Return number of jobs.
    return _numFadeJobs;
}

void _deleteFromJobs(int indexToDelete) {
    static int i = 0;
    int finalIndex = _numFadeJobs - 1;
    delete (_fadeJobs[indexToDelete]);
    for (i = indexToDelete; i < finalIndex; i++) {
        _fadeJobs[i] = _fadeJobs[i + 1];
    }
    _fadeJobs[finalIndex] = NULL;
    _numFadeJobs--;
}

void fade() {
    static int i = 0;
    static int isCompleted = 0;

    // For each job, get the job and fade it. If the job is completed,
    // remove it from the list of jobs.
    i = 0;
    while (i < _numFadeJobs) {
        // Get the job and fade it.
        isCompleted = _fadeJobs[i]->stepFade();

        // Remove from queue if it's done.
        if (isCompleted) {
            _deleteFromJobs(i);
            continue;
        }
        i++;
    }
    return;
}

int getNumFadeJobs() {
    return _numFadeJobs;
}

int fade_DEPRECATED() {
    fade();
    return getNumFadeJobs();
}

FadeJob::FadeJob(int initialValue, int finalValue, int numberSteps,
                 void (*callback)(int)) {
    _initialValue = initialValue;
    _finalValue = finalValue;
    _currentStep = 1;
    _numberSteps = numberSteps;
    _callback = callback;
}

int FadeJob::stepFade() {
    static int level;
    int deltaY = _finalValue - _initialValue;
    level = (double)deltaY * _currentStep / _numberSteps + _initialValue;
    _callback(level);
    if (_currentStep++ >= _numberSteps) {
        return 1;
    }
    return 0;
}
