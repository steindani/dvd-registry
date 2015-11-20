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
							(data: dvdApp.Services.FragmentResult) => {
								$scope.firstResult = data.first_result;

								if ($scope.selectedId !== data.first_result.id) {
									$scope.possibleMovies = data.results;
								}
							})
					},
					200
				);
			}

			$scope.selectPossibleMovie = function(id: string) {
				$scope.possibleMovies.forEach(element => {
					if (element.id === id) {
						$scope.enteredTitle = element.title;
						$scope.selectedId = id;
						$scope.possibleMovies = [];

						$scope.titleChanged();
					}
				});
			}
			
			$scope.addSelectedMovie = () => {
				BackendService.addMovie($scope.selectedId, $scope.enteredTitle, $scope.medium, null);
			}
		}
	}

    angular
        .module('dvdApp.Controllers', [])
        .controller('NewMovieController', ['$scope', '$window', '$http', '$q', 'ngDialog', '$auth', '$timeout', dvdApp.Controllers.NewMovieController]);

    export interface INewMovieScope extends ng.IScope {
		enteredTitle: string;
		selectedId: string;
		possibleMovies: { id: string, title: string }[];
		firstResult: any;
		media: string[];
		medium: string;

        titleChanged: () => void;
		selectPossibleMovie: (id: string) => void;
		addSelectedMovie: () => void;
    }
}
