/// <reference path="../../_all.ts" />
'use strict';

module dvdApp.Controllers {
    export class MoviesController {

        scope: any;

        constructor(
            private $scope: IMoviesScope,
            private $window: ng.IWindowService,
            private $http: ng.IHttpService,
            private ngDialog: angular.dialog.IDialogService,
            private $auth: any,
            private BackendService: dvdApp.Services.BackendService
        ) {
            this.scope = $scope;
            
            BackendService.movies((data) => {$scope.movies = data});
            BackendService.recommendations((data) => {$scope.recommendations = data});

            $scope.showDetails = function(id: string) {
                var childScope: any = $scope.$new();
                BackendService.movieDetail(id, (data:dvdApp.Services.MovieDetail) => {
                    childScope.movie = data;
                });

                ngDialog.open({
                    className: 'ngdialog-theme-dvd',
                    template: 'views/details.html',
                    plain: false,
                    scope: childScope
                });
            }
            
            $scope.newMovieModal = function() {
                ngDialog.open({
                    className: 'ngdialog-theme-dvd',
                    template: 'views/newMovieModal.html',
                    plain: false,
                    controller: dvdApp.Controllers.NewMovieController,
                    scope: $scope
                });
            }
            
            $scope.applyUpdate = function(movie: dvdApp.Services.MoviePresent) {
                $scope.movies.push(movie);
            }
            
        }
    }

    angular
        .module('dvdApp.Controllers', [])
        .controller('MoviesController', ['$scope', '$window', '$http', 'ngDialog', '$auth', 'BackendService', dvdApp.Controllers.MoviesController]);

    export interface IMoviesScope extends ng.IScope {
        movies: dvdApp.Services.MoviePresent[];
        recommendations: dvdApp.Services.MoviePresent[];

        showDetails: (id: string) => void;
        newMovieModal: () => void;
        applyUpdate: (movie: dvdApp.Services.MoviePresent) => void;
    }
}
