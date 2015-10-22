/// <reference path="../../_all.ts" />
'use strict';

module dvdApp.Controllers {

    export class MoviesCtrl {

        scope: any;
        data: any;

        constructor(
            private $scope: ng.IScope
        ) {
            this.scope = $scope;
            this.data = {
                movies: [
                    {
                        title: "The Fifth Element",
                        cover: "https://image.tmdb.org/t/p/w185/zaFa1NRZEnFgRTv5OVXkNIZO78O.jpg"
                    }
                ]
            };
        }
    }

    angular
      .module('dvdApp.Controllers', [])
      .controller('MoviesCtrl', ['$scope', dvdApp.Controllers.MoviesCtrl]);
}
