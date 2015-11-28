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
            private BackendService: dvdApp.Services.BackendService,
            private $timeout: ng.ITimeoutService
        ) {
            this.scope = $scope;
            $scope.ord = '$index';
            $scope.reverse = false;

            var updateMovies = () => {
                BackendService.movies((data) => { $scope.movies = data });
            }

            var updateRecommendations = () => {
                BackendService.recommendations((data) => { $scope.recommendations = data });
            }

            updateMovies();
            updateRecommendations();

            $scope.showDetails = function(id: string) {
                var childScope: any = $scope.$new();
                BackendService.movieDetail(id, (data: dvdApp.Services.MovieDetail) => {
                    childScope.movie = data;
                });

                ngDialog.open({
                    className: 'ngdialog-theme-dvd',
                    template: 'views/details.html',
                    plain: false,
                    scope: childScope
                });

                updateRecommendations();
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
                $timeout(() => {
                    $scope.movies.push(movie);
                    updateRecommendations();
                });
            }

            var filterTimeoutPromise;
            $scope.updateFilter = function() {
                if (filterTimeoutPromise) {
                    $timeout.cancel(filterTimeoutPromise)
                }

                filterTimeoutPromise = $timeout(
                    () => {
                        BackendService.updateFilter($scope.search)
                    },
                    300
                );
            }

            $scope.first = (array: any[]) => {
                return array[0];
            }
        }
    }

    angular
        .module('dvdApp.Controllers', [])
        .controller('MoviesController', ['$scope', '$window', '$http', 'ngDialog', '$auth', 'BackendService', '$timeout', dvdApp.Controllers.MoviesController]);

    export interface IMoviesScope extends ng.IScope {
        movies: dvdApp.Services.MoviePresent[];
        recommendations: dvdApp.Services.MoviePresent[];
        search: string;

        ord: string;
        reverse: boolean;
        first: <T> (array: T[]) => T;

        showDetails: (id: string) => void;
        newMovieModal: () => void;
        applyUpdate: (movie: dvdApp.Services.MoviePresent) => void;

        // filteredMovies: (movies: dvdApp.Services.MoviePresent[], search: string) => void;
        updateFilter: () => void;
    }
}
