/// <reference path="../../_all.ts" />
'use strict';

module dvdApp.Controllers {
    export class MoviesCtrl {
        
        scope: any;

        constructor(
            private $scope: IMoviesScope,
            private $window: ng.IWindowService,
            private $http: ng.IHttpService
        ) {
            this.scope = $scope;
            $scope.movies = [];
            $http.get("http://api.themoviedb.org/3/discover/movie?api_key=13ed7e5e07699386ba2c32a52aed7ae6")
                 .success((data) =>{
                     (<any> data).results.slice(4).forEach(movie => {
                         var m = {
                             id: $scope.movies.length,
                             title: movie.original_title,
                             cover: "https://image.tmdb.org/t/p/w185" + movie.poster_path
                         };
                         console.log(m);
                         $scope.movies.push(m);
                     });
                 });
                 
            $scope.recommendations = [];
            $http.get("http://api.themoviedb.org/3/discover/movie?api_key=13ed7e5e07699386ba2c32a52aed7ae6")
                 .success((data) =>{
                     (<any> data).results.slice(0, 4).forEach(movie => {
                         var m = {
                             id: $scope.recommendations.length,
                             title: movie.original_title,
                             cover: "https://image.tmdb.org/t/p/w185" + movie.poster_path
                         };
                         console.log(m);
                         $scope.recommendations.push(m);
                     });
                 });
        }
    }

    angular
      .module('dvdApp.Controllers', [])
      .controller('MoviesCtrl', ['$scope', '$window', '$http', dvdApp.Controllers.MoviesCtrl]);
    
    export interface IMoviesScope extends ng.IScope {
        movies: any;
        recommendations: any;
    }
}
