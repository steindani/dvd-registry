/// <reference path="../../_all.ts" />
'use strict';
var dvdApp;
(function (dvdApp) {
    var Controllers;
    (function (Controllers) {
        var MoviesCtrl = (function () {
            function MoviesCtrl($scope, $window, $http, ngDialog) {
                this.$scope = $scope;
                this.$window = $window;
                this.$http = $http;
                this.ngDialog = ngDialog;
                this.scope = $scope;
                $scope.movies = [];
                $http.get("http://api.themoviedb.org/3/discover/movie?api_key=13ed7e5e07699386ba2c32a52aed7ae6")
                    .success(function (data) {
                    data.results.slice(4).forEach(function (movie) {
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
                    .success(function (data) {
                    data.results.slice(0, 4).forEach(function (movie) {
                        var m = {
                            id: movie.id,
                            title: movie.original_title,
                            cover: "https://image.tmdb.org/t/p/w185" + movie.poster_path
                        };
                        console.log(m);
                        $scope.recommendations.push(m);
                    });
                });
                $scope.showDetails = function (id) {
                    ngDialog.open({
                        template: 'views/details.html',
                        plain: false
                    });
                };
            }
            return MoviesCtrl;
        })();
        Controllers.MoviesCtrl = MoviesCtrl;
        angular
            .module('dvdApp.Controllers', [])
            .controller('MoviesCtrl', ['$scope', '$window', '$http', 'ngDialog', dvdApp.Controllers.MoviesCtrl]);
    })(Controllers = dvdApp.Controllers || (dvdApp.Controllers = {}));
})(dvdApp || (dvdApp = {}));
//# sourceMappingURL=MoviesCtrl.js.map