/*
 **********************************************************************
 *  File   : app.js
 *  Author : peach
 *  Date   : 8 July 2019
 **********************************************************************
 */

// Create the app module.
var SmartHome = angular.module('SmartHomeApp', ['ngRoute', 'ui.bootstrap']);

// Configure the routing table.
SmartHome.config(function($routeProvider, $locationProvider) {
    $routeProvider
        .when('/home', {
            templateUrl: 'html/views/home.html',
        })
        .when('/sandbox', {
            templateUrl: 'html/views/sandbox.html',
            controller: 'SandboxController'
        })
        .otherwise({
            templateUrl: 'html/views/home.html',
        });
    // Use the HTML5 History API
    $locationProvider.hashPrefix('');
});

/*
 * Joke interface for turning on green light as a demo.
 */
SmartHome.controller('SandboxController', ['$scope', 'constants', 'PeripheralAPIService',
    function($scope, constants, PeripheralAPIService) {
        $scope.fire = function() {
            PeripheralAPIService.setPeripheralState(3, {
                level: 255
            }).then(function(result) {
                console.log('Green Light should now be on.');
            }, function(error) {
                console.error(error);
            });
        };
    }
]);


SmartHome.controller('PeriperalListController', ['$uibModal', '$scope', '$interval', 'constants', 'PeripheralAPIService',
    function($uibModal, $scope, $interval, constants, PeripheralAPIService) {
        $scope.peripherals = [];
        $scope.columnNames = ['Name', 'Type', 'State', 'Configure'];
        $scope.refreshPeripherals = function() {
            PeripheralAPIService.getPeripherals().then(function(result) {
                $scope.peripherals = result;
            }, function(error) {
                console.error(error);
            });
        };
        $scope.getHumanReadableState = function(peripheral) {
            var state = peripheral.state;
            var result = '';
            switch (peripheral.type) {
                case constants.PERIPHERAL_TYPE_ONOFF:
                    result = (state.enabled ? 'On' : 'Off');
                    break;
                case constants.PERIPHERAL_TYPE_SLIDER:
                    result = (state.level == 0 ? 'Disabled' : state.level);
                    break;
                case constants.PERIPHERAL_TYPE_RGB:
                    result = state.r + " " + state.g + " " + state.b;
                    break;
            };
            return result;
        };

        $scope.openStateDialog = function(peripheral) {
            $uibModal.open({
                templateUrl: 'html/views/modals/set_state_dialog.html',
                controller: 'SetStateDialog',
                size: 'md',
                windowClass: 'popup-modal',
                backdrop: 'static',
                resolve: {
                    peripheral: function() {
                        return peripheral;
                    },
                    constants: function() {
                        return constants;
                    }
                }
            }).result.then(function(newState) {
                PeripheralAPIService.setPeripheralState(peripheral.id, newState).then(function(result) {
                    $scope.refreshPeripherals();
                }, function(error) {
                    console.error(error);
                });
            }, function(error) {
                console.error(error);
            });
        };

        $interval($scope.refreshPeripherals, constants.TABLE_REFRESH_RATE);
        $scope.refreshPeripherals();
    }
]);

SmartHome.controller('PresetListController', ['$scope', '$interval', 'constants', 'PresetAPIService',
    function($scope, $interval, constants, PresetAPIService) {

        $scope.presets = [];

        $scope.applyPreset = function(preset) {
            PresetAPIService.applyPreset(preset.id).then(function(result) {
            }, function(error) {
                console.error(error);
            });
        };
        $scope.refreshPresets = function() {
            PresetAPIService.getPresets().then(function(result) {
                $scope.presets = result;
            }, function(error) {
                console.error(error);
            });
        };

        $interval($scope.refreshPresets, constants.TABLE_REFRESH_RATE);
        $scope.refreshPresets();
    }
]);

SmartHome.controller('ScheduleListController', ['$scope', '$interval', 'constants', 'ScheduleAPIService',
    function($scope, $interval, constants, ScheduleAPIService) {

        $scope.schedules = [];
        $scope.columnNames = ['Name', 'Enabled'];

        $scope.toggle = function(schedule) {
            var newState = schedule.is_enabled ? false : true;
            schedule.is_enabled = newState;
            ScheduleAPIService.setScheduleEnabled(schedule.id, newState).then(function(result){
            }, function(error) {
                console.error(error);
            });
        };
        $scope.refreshSchedules = function() {
            ScheduleAPIService.getSchedules().then(function(result) {
                $scope.schedules = result;
            }, function(error) {
                console.error(error);
            });
        };

        $interval($scope.refreshSchedules, constants.TABLE_REFRESH_RATE);
        $scope.refreshSchedules();
    }
]);

SmartHome.controller('SetStateDialog', ['$scope', '$uibModalInstance', 'peripheral', 'constants',
    function($scope, $uibModalInstance, peripheral, constants) {
        $scope.constants = constants;
        $scope.peripheral = peripheral;
        $scope.onOffOptions = [{
            name: 'On',
            value: true
        }, {
            name: 'Off',
            value: false
        }, ];
        $scope.state = peripheral.state;

        $scope.cancel = function() {
            $uibModalInstance.dismiss('cancel');
        };
        $scope.submit = function() {
            $uibModalInstance.close($scope.state);
        };
    }
]);

SmartHome.factory('PeripheralAPIService', ['$http', '$q',
    function($http, $q) {
        function getPeripherals() {
            var deferred = $q.defer();
            $http.get("/api/peripherals", {}).then(function(result) {
                deferred.resolve(result.data);
            }, function(error) {
                deferred.reject(error);
            });
            return deferred.promise;
        };

        function setPeripheralSchedule(peripheralId, scheduleId) {
            var payload = {
                peripheral_id: peripheralId,
                schedule_id: scheduleId,
            };
            var deferred = $q.defer();
            $http.post("/api/peripheral_schedule", payload).then(function(result) {
                deferred.resolve(result.data);
            }, function(error) {
                deferred.reject(error);
            });
            return deferred.promise;
        }

        function setPeripheralState(peripheralId, state) {
            var payload = {
                peripheral_id: peripheralId,
                state: state,
            };
            var deferred = $q.defer();
            $http.post("/api/peripheral_state", payload).then(function(result) {
                deferred.resolve(result.data);
            }, function(error) {
                deferred.reject(error);
            });
            return deferred.promise;
        }
        return {
            getPeripherals: getPeripherals,
            setPeripheralSchedule: setPeripheralSchedule,
            setPeripheralState: setPeripheralState,
        };
    }
]);

SmartHome.factory('PresetAPIService', ['$http', '$q',
    function($http, $q) {
        function getPresets() {
            var deferred = $q.defer();
            $http.get("/api/presets", {}).then(function(result) {
                deferred.resolve(result.data);
            }, function(error) {
                deferred.reject(error);
            });
            return deferred.promise;
        };

        function applyPreset(preset_id) {
            var payload = {
                preset_id: preset_id,
            };
            var deferred = $q.defer();
            $http.post("/api/preset", payload).then(function(result) {
                deferred.resolve(result.data);
            }, function(error) {
                deferred.reject(error);
            });
            return deferred.promise;
        }

        return {
            applyPreset: applyPreset,
            getPresets: getPresets,
        };
    }
]);

SmartHome.factory('ScheduleAPIService', ['$http', '$q',
    function($http, $q) {
        function getSchedules() {
            var deferred = $q.defer();
            $http.get("/api/schedules", {}).then(function(result) {
                deferred.resolve(result.data);
            }, function(error) {
                deferred.reject(error);
            });
            return deferred.promise;
        };

        function setScheduleEnabled(schedule_id, is_enabled) {
            var payload = {
                schedule_id: schedule_id,
                is_enabled: is_enabled
            };
            var deferred = $q.defer();
            $http.post("/api/schedule_enabled", payload).then(function(result) {
                deferred.resolve(result.data);
            }, function(error) {
                deferred.reject(error);
            });
            return deferred.promise;
        }

        return {
            getSchedules: getSchedules,
            setScheduleEnabled: setScheduleEnabled
        };
    }
]);

SmartHome.constant('constants', {
    PERIPHERAL_TYPE_ONOFF: "ONOFF",
    PERIPHERAL_TYPE_SLIDER: "SLIDER",
    PERIPHERAL_TYPE_RGB: "RGB",
    PERIPHERAL_MODE_DISABLED: "DISABLED",
    PERIPHERAL_MODE_SCHEDULED: "SCHEDULED",
    PERIPHERAL_MODE_FIXED: "FIXED",
    TABLE_REFRESH_RATE: 10000,
});
/*
 *
 *
 *
 *
 *
 *
 *
 *
 *
 *
 */