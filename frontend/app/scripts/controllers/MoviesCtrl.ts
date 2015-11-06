/// <reference path="../../_all.ts" />
'use strict';

module dvdApp.Controllers {
    export class MoviesCtrl {
        
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
                 .success((data) =>{
                     (<any> data).results.slice(4).forEach(movie => {
                         var m = {
                             id: movie.id,
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
                             id: movie.id,
                             title: movie.original_title,
                             cover: "https://image.tmdb.org/t/p/w185" + movie.poster_path
                         };
                         console.log(m);
                         $scope.recommendations.push(m);
                     });
                 });
            
            $scope.showDetails = function (id: string) {
                ngDialog.open({
                    template: '<p>' + id + '</p>',
                    plain: true
                });
            }
        }
    }

    angular
      .module('dvdApp.Controllers', [])
      .controller('MoviesCtrl', ['$scope', '$window', '$http', 'ngDialog', dvdApp.Controllers.MoviesCtrl]);
    
    export interface IMoviesScope extends ng.IScope {
        movies: any;
        recommendations: any;
        
        showDetails: (id: string) => void;
    }
}
