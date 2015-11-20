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
        'satellizer',
        'dvdApp.Controllers',
        'dvdApp.Directives',
        'dvdApp.Services'
    ]);
    app.config(function ($routeProvider) {
        $routeProvider
            .when('/', {
            templateUrl: 'views/main.html',
            controller: dvdApp.Controllers.MoviesController,
            controllerAs: 'controller'
        })
            .when('/login', {
            templateUrl: 'views/login.html',
            controller: dvdApp.Controllers.LoginController,
            controllerAs: 'controller'
        })
            .otherwise({
            redirectTo: '/'
        });
    });
    // http://stackoverflow.com/questions/11541695/redirecting-to-a-certain-route-based-on-condition
    app.run(function ($rootScope, $location, $auth) {
        // register listener to watch route changes
        $rootScope.$on("$routeChangeStart", function (event, next, current) {
            if (!$auth.isAuthenticated()) {
                // no logged user, we should be going to #login
                if (next.templateUrl === "views/login.html") {
                }
                else {
                    // not going to #login, we should redirect now
                    $location.path("/login");
                }
            }
        });
    });
    app.config(function ($authProvider) {
        $authProvider.httpInterceptor = false;
        $authProvider.baseUrl = "http://localhost:5000";
        $authProvider.google({
            clientId: '1085060587208-7ciq58jrnui1go17k7o8fuqu14281jdu.apps.googleusercontent.com'
        });
    });
    // app.config(['$httpProvider', '$authProvider', function($httpProvider, config) {
    //     $httpProvider.interceptors.push(['$q', function($q) {
    //       var tokenName = config.tokenPrefix ? config.tokenPrefix + '_' + config.tokenName : config.tokenName;
    //       return {
    //         request: function(httpConfig) {
    //           if (localStorage.getItem(tokenName)) {
    //             httpConfig.headers.Authorization = 'Bearer ' + localStorage.getItem(tokenName);
    //           }
    //           return httpConfig;
    //         },
    //         responseError: function(response) {
    //           if (response.status === 401) {
    //             localStorage.removeItem(tokenName);
    //           }
    //           return $q.reject(response);
    //         }
    //       };
    //     }]);
    //   }]);
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
    // http://stackoverflow.com/questions/24163152/angularjs-ng-src-inside-of-iframe
    app.filter('trustAsResourceUrl', ['$sce', function ($sce) {
            return function (val) {
                return $sce.trustAsResourceUrl(val);
            };
        }]);
})(dvdApp || (dvdApp = {}));
//# sourceMappingURL=app.js.map