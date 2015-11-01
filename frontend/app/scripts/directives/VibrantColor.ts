/// <reference path="../../_all.ts" />
'use strict';

declare var Vibrant;

module dvdApp.Directives {

	export function VibrantColor() {
		return {
			restrict: 'AEC',

			link: function(
				scope: IVibrantScope,
				element: JQuery
			) {
				scope.$watch('m', () => {
					var image = $(element).children('img.cover-loader');
					(<any> image).crossOrigin = "Anonymous";
					
					image.on(
						'load',
						(event: JQueryEventObject) => {
							//var vibrant = new Vibrant((<any> event).target);
							//element.append(vibrant.swatches());
						});
				});

			}
		}
	}

	angular.module('dvdApp.Directives', [])
		.directive('vibrantColor', dvdApp.Directives.VibrantColor);

	export interface IVibrantScope extends ng.IScope {
		vibrant: any;
		m: any;
	}
}