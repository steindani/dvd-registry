/// <reference path="../../_all.ts" />
'use strict';

module dvdApp.Controllers {
    export class LoginController {

        scope: any;

        constructor(
            private $scope: ILoginScope,
            private $auth: any,
            private $location: ng.ILocationService,
            private $routeParams: any
        ) {
            this.scope = $scope;

            $scope.authenticate = function(provider) {
                $auth.authenticate(provider)
                    .then((response) => {
                        $auth.setToken(response.data.token);
                        $location.url("/");
                    })
                    .catch((data) => {
                        $location.url("login?force=" + provider);
                    });
            };

            $scope.isAuthenticated = () => {
                return $auth.isAuthenticated();
            }

            $scope.logOut = () => {
                $auth.removeToken();
                $location.url("/");
            }

            console.log($routeParams);
            if ($routeParams.force) {
                $scope.authenticate($routeParams.force)
            }
        }
    }

    angular
        .module('dvdApp.Controllers', [])
        .controller('LoginController', ['$scope', '$auth', '$location', '$routeParams', dvdApp.Controllers.LoginController]);

    export interface ILoginScope extends ng.IScope {
        authenticate: (provider: string) => void;
        isAuthenticated: () => boolean;
        logOut: () => void;
    }
}
