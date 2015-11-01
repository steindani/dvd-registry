/// <reference path="../../_all.ts" />
'use strict';

module dvdApp.Controllers {
    export class MoviesCtrl {
        
        scope: any;

        constructor(
            private $scope: IMoviesScope,
            private $window: ng.IWindowService
        ) {
            this.scope = $scope;
            $scope.movies = [
                    {
                        title: "The Fifth Element",
                        cover: "https://image.tmdb.org/t/p/w185/zaFa1NRZEnFgRTv5OVXkNIZO78O.jpg"
                    },
                    {
                        title: "The Fifth Element",
                        cover: "https://image.tmdb.org/t/p/w185/zaFa1NRZEnFgRTv5OVXkNIZO78O.jpg"
                    }
                ];
        }
    }

    angular
      .module('dvdApp.Controllers', [])
      .controller('MoviesCtrl', ['$scope', '$window', dvdApp.Controllers.MoviesCtrl]);
    
    export interface IMoviesScope extends ng.IScope {
        movies: any;
    }
}
