/// <reference path="../../_all.ts" />
'use strict';

module dvdApp.Controllers {
    export class NewMovieController {

        scope: any;

        constructor(
            private $scope: INewMovieScope,
            private ngDialog: angular.dialog.IDialogService,
			private BackendService: dvdApp.Services.IBackendService,
			private $timeout: ng.ITimeoutService
        ) {
            this.scope = $scope;

			$scope.enteredTitle = ""
			$scope.firstResult = {}

			BackendService.media((data: any) => { $scope.media = data.media });

			var titleTimeoutPromise;
			$scope.titleChanged = function() {
				if (titleTimeoutPromise) {
					$timeout.cancel(titleTimeoutPromise)
				}

				titleTimeoutPromise = $timeout(
					() => {
						BackendService.searchFor(
							$scope.enteredTitle,
							(data: { id: string, title: string }[]) => {
								$scope.possibleMovies = data;
								console.log(data);
							})
					},
					200
				);
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
        .controller('NewMovieController', ['$scope', '$window', '$http', '$q', 'ngDialog', '$auth', '$timeout', dvdApp.Controllers.NewMovieController]);

    export interface INewMovieScope extends ng.IScope {
		enteredTitle: string;
		possibleMovies: { id: string, title: string }[];
		firstResult: any;
		media: string[];

        titleChanged: () => void;
		selectPossibleMovie: (id: string) => void;
    }
}
