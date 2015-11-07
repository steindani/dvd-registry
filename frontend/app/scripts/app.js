/// <reference path="../_all.ts" />
'use strict';
var dvdApp;
(function (dvdApp) {
    var app = angular
        .module('dvdApp', [
        'ngAnimate',
        'ngCookies',
        'ngResource',
        'ngRoute',
        'ngSanitize',
        'ngTouch',
        'ngDialog',
        'dvdApp.Controllers',
        'dvdApp.Directives'
    ]);
    app.config(function ($routeProvider) {
        $routeProvider
            .when('/', {
            templateUrl: 'views/main.html',
            controller: dvdApp.Controllers.MoviesController,
            controllerAs: 'controller'
        })
            .otherwise({
            redirectTo: '/'
        });
    });
    app.config(["ngDialogProvider", function (ngDialogProvider) {
            ngDialogProvider.setDefaults({
                className: "ngdialog-theme-default",
                plain: false,
                showClose: true,
                closeByDocument: true,
                closeByEscape: true,
                appendTo: false
            });
        }]);
})(dvdApp || (dvdApp = {}));
//# sourceMappingURL=app.js.map