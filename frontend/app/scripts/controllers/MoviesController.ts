/// <reference path="../../_all.ts" />
'use strict';

module dvdApp.Controllers {
    export class MoviesController {

        scope: any;

        constructor(
            private $scope: IMoviesScope,
            private $window: ng.IWindowService,
            private $http: ng.IHttpService,
            private ngDialog: angular.dialog.IDialogService
        ) {
            this.scope = $scope;
            $scope.movies = [];
            $http.get("http://api.themoviedb.org/3/discover/movie?api_key=13ed7e5e07699386ba2c32a52aed7ae6")
                .success((data) => {
                    (<any>data).results.slice(4).forEach(movie => {
                        var m = {
                            id: movie.id,
                            title: movie.original_title,
                            cover: "https://image.tmdb.org/t/p/w185" + movie.poster_path,
                            backdrop: "https://image.tmdb.org/t/p/original" + movie.backdrop_path
                        };
                        console.log(m);
                        $scope.movies.push(m);
                    });
                });

            $scope.recommendations = [];
            $http.get("http://api.themoviedb.org/3/discover/movie?api_key=13ed7e5e07699386ba2c32a52aed7ae6")
                .success((data) => {
                    (<any>data).results.slice(0, 4).forEach(movie => {
                        var m = {
                            id: movie.id,
                            title: movie.original_title,
                            cover: "https://image.tmdb.org/t/p/w185" + movie.poster_path
                        };
                        console.log(m);
                        $scope.recommendations.push(m);
                    });
                });

            $scope.showDetails = function(id: string) {
                var movie : any = $scope.movies.find(m => m.id === id);
                
                var childScope: any = $scope.$new();              
                childScope.movie = {
                    title: movie.title,
                    backdrop:  movie.backdrop,                    
                }

                ngDialog.open({
                    className: 'ngdialog-theme-dvd',
                    template: 'views/details.html',
                    plain: false,
                    scope: childScope
                });
            }
        }
    }

    angular
        .module('dvdApp.Controllers', [])
        .controller('MoviesController', ['$scope', '$window', '$http', 'ngDialog', dvdApp.Controllers.MoviesController]);

    export interface IMoviesScope extends ng.IScope {
        movies: any;
        recommendations: any;

        showDetails: (id: string) => void;
    }
}
