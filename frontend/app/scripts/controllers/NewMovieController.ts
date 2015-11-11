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
            private ngDialog: angular.dialog.IDialogService
        ) {
            this.scope = $scope;

			$scope.enteredTitle = ""
			$scope.firstResult = {}

			$scope.titleChanged = function() {
				while($scope.possibleMovies && $scope.possibleMovies.length !== 0) {
					$scope.possibleMovies.pop();
				}
				
				$http.post(
					"http://127.0.0.1:5000/helper/search",
					{ fragment: $scope.enteredTitle }
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
        .controller('NewMovieController', ['$scope', '$window', '$http', '$q', 'ngDialog', dvdApp.Controllers.NewMovieController]);

    export interface INewMovieScope extends ng.IScope {
		enteredTitle: string;
		possibleMovies: [{ id: string, title: string }];
		firstResult: any;

        titleChanged: () => void;
		selectPossibleMovie: (id: string) => void;
    }
}
