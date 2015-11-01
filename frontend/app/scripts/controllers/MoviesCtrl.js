/// <reference path="../../_all.ts" />
'use strict';
var dvdApp;
(function (dvdApp) {
    var Controllers;
    (function (Controllers) {
        var MoviesCtrl = (function () {
            function MoviesCtrl($scope, $window, $http) {
                this.$scope = $scope;
                this.$window = $window;
                this.$http = $http;
                this.scope = $scope;
                $scope.movies = [];
                $http.get("http://api.themoviedb.org/3/discover/movie?api_key=13ed7e5e07699386ba2c32a52aed7ae6")
                    .success(function (data) {
                    data.results.slice(4).forEach(function (movie) {
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
                    .success(function (data) {
                    data.results.slice(0, 4).forEach(function (movie) {
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
            return MoviesCtrl;
        })();
        Controllers.MoviesCtrl = MoviesCtrl;
        angular
            .module('dvdApp.Controllers', [])
            .controller('MoviesCtrl', ['$scope', '$window', '$http', dvdApp.Controllers.MoviesCtrl]);
    })(Controllers = dvdApp.Controllers || (dvdApp.Controllers = {}));
})(dvdApp || (dvdApp = {}));
//# sourceMappingURL=MoviesCtrl.js.map