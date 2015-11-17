/// <reference path="../../_all.ts" />
'use strict';

module dvdApp.Controllers {
    export class NewMovieController {

        scope: any;

        constructor(
            private $scope: INewMovieScope,
            private $window: ng.IWindowService,
            private $http: ng.IHttpService,
			private $q: ng.IQService,
            private ngDialog: angular.dialog.IDialogService,
			private $auth: any
        ) {
            this.scope = $scope;

			$scope.enteredTitle = ""
			$scope.firstResult = {}
			
			$http({
				method: "GET",
				url: "http://localhost:5000/media",
				headers: {
					Authorization: 'Bearer ' + $auth.getToken()
				}
			}
			).success((data) => {
				$scope.media = (<any>data).media;
			});

			$scope.titleChanged = function() {
				// var deferred = $q.defer();
				
				while($scope.possibleMovies && $scope.possibleMovies.length !== 0) {
					$scope.possibleMovies.pop();
				}
				
				$http({
					method: "POST",
					url: "http://127.0.0.1:5000/helper/search",
					data: {
						fragment: $scope.enteredTitle
					},
					headers: {
						Authorization: 'Bearer ' + $auth.getToken()
					}			
				}
				).success((data) => {
					if ((<any>data).possible_ids) {
						$scope.possibleMovies = (<any>data).possible_ids.map(
							(value, index) => {
								return {
									id: value,
									title: (<any>data).possible_titles[index]
								}
							});
					}
				});
			}
			
			$scope.selectPossibleMovie = function(id: string) {
				$scope.possibleMovies.forEach(element => {
					if (element.id === id.toString()) {
						$scope.enteredTitle = element.title;
					}
				});
			}
		}
	}

    angular
        .module('dvdApp.Controllers', [])
        .controller('NewMovieController', ['$scope', '$window', '$http', '$q', 'ngDialog', '$auth', dvdApp.Controllers.NewMovieController]);

    export interface INewMovieScope extends ng.IScope {
		enteredTitle: string;
		possibleMovies: [{ id: string, title: string }];
		firstResult: any;
		media: [string];

        titleChanged: () => void;
		selectPossibleMovie: (id: string) => void;
    }
}
