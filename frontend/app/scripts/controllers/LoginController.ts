/// <reference path="../../_all.ts" />
'use strict';

module dvdApp.Controllers {
    export class LoginController {

        scope: any;

        constructor(
            private $scope: ILoginScope,
            private $auth: any,
            private $location: ng.ILocationService
        ) {
            this.scope = $scope;

            $scope.authenticate = function(provider) {
                $auth.authenticate(provider)
                    .then((response) => {
                        $auth.setToken(response.data.token);
                        $location.url("/");
                    });
            };

            $scope.isAuthenticated = () => {
                return $auth.isAuthenticated();
            }

            $scope.logOut = () => {
                $auth.removeToken();
                $location.url("/");
            }
        }
    }

    angular
        .module('dvdApp.Controllers', [])
        .controller('LoginController', ['$scope', '$auth', '$location', dvdApp.Controllers.LoginController]);

    export interface ILoginScope extends ng.IScope {
        authenticate: (provider: string) => void;
        isAuthenticated: () => boolean;
        logOut: () => void;
    }
}
