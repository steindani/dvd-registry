/// <reference path="../_all.ts" />
var dvdApp;
(function (dvdApp) {
    'use strict';
    /**
    * @ngdoc overview
    * @name dvdApp
    * @description
    * # dvdApp
    *
    * Main module of the application.
    */
    angular.module('dvdApp.Controllers', []);
    angular
        .module('dvdApp', [
        'ngAnimate',
        'ngCookies',
        'ngResource',
        'ngRoute',
        'ngSanitize',
        'ngTouch',
        'dvdApp.Controllers'
    ])
        .config(function ($routeProvider) {
        $routeProvider
            .when('/', {
            templateUrl: 'views/main.html',
            controller: 'MoviesCtrl',
            controllerAs: 'main'
        })
            .when('/about', {
            templateUrl: 'views/about.html',
            controller: 'AboutCtrl',
            controllerAs: 'about'
        })
            .otherwise({
            redirectTo: '/'
        });
    });
    angular
        .module('dvdApp.Controllers')
        .controller('MoviesCtrl', ['$scope']);
})(dvdApp || (dvdApp = {}));
//# sourceMappingURL=app.js.map