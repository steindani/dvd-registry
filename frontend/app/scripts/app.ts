/// <reference path="../_all.ts" />
'use strict';

module dvdApp {

  var app = angular
    .module('dvdApp', [
    'ngAnimate',
    'ngCookies',
    'ngResource',
    'ngRoute',
    'ngSanitize',
    'ngTouch',
    'dvdApp.Controllers',
    'dvdApp.Directives'
  ]);

  app.config(
      function($routeProvider) {
        $routeProvider
          .when('/', {
            templateUrl: 'views/main.html',
            controller: dvdApp.Controllers.MoviesCtrl,
            controllerAs: 'controller'
          })
          .otherwise({
            redirectTo: '/'
          });
        }
      );
}