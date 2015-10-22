/// <reference path="../_all.ts" />
'use strict';
var dvdApp;
(function (dvdApp) {
    //export module Controllers {}
    //angular.module('dvdApp.Controllers', []);
    var app = angular
        .module('dvdApp', [
        'ngAnimate',
        'ngCookies',
        'ngResource',
        'ngRoute',
        'ngSanitize',
        'ngTouch',
        'dvdApp.Controllers'
    ]);
    app.config(function ($routeProvider) {
        $routeProvider
            .when('/', {
            templateUrl: 'views/main.html',
            controller: dvdApp.Controllers.MoviesCtrl,
            controllerAs: 'movies'
        })
            .otherwise({
            redirectTo: '/'
        });
    });
})(dvdApp || (dvdApp = {}));
//# sourceMappingURL=app.js.map