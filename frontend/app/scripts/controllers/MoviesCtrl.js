/// <reference path="../../_all.ts" />
'use strict';
var dvdApp;
(function (dvdApp) {
    var Controllers;
    (function (Controllers) {
        var MoviesCtrl = (function () {
            function MoviesCtrl($scope) {
                this.$scope = $scope;
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
            return MoviesCtrl;
        })();
        Controllers.MoviesCtrl = MoviesCtrl;
        angular
            .module('dvdApp.Controllers', [])
            .controller('MoviesCtrl', ['$scope', dvdApp.Controllers.MoviesCtrl]);
        angu;
    })(Controllers = dvdApp.Controllers || (dvdApp.Controllers = {}));
})(dvdApp || (dvdApp = {}));
//# sourceMappingURL=MoviesCtrl.js.map