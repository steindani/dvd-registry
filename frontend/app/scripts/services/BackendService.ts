/// <reference path="../../_all.ts" />
'use strict';

module dvdApp.Services {
    export class BackendService implements IBackendService {

        private static MEDIA_URI: string = "http://localhost:5000/media";
        private static HELPER_SEARCH_URI: string = "http://127.0.0.1:5000/helper/search";

        private static MOCK = true;

        constructor(
            private $http: ng.IHttpService,
            private $q: ng.IQService,
            private $auth: any
        ) {
            this.$http = $http;
            this.$q = $q;
            this.$auth = $auth;
        }

        public movies(callback: (data: MoviePresent[]) => void) {
            if (BackendService.MOCK) {
                this.$http.get("http://api.themoviedb.org/3/discover/movie?api_key=13ed7e5e07699386ba2c32a52aed7ae6")
                    .success(
                    (data: any) => {
                        callback(data.results.slice(4).map(movie => {
                            var m = new dvdApp.Services.MoviePresent();
                            m.id = movie.id;
                            m.title = movie.original_title;
                            m.poster_path = "https://image.tmdb.org/t/p/w185" + movie.poster_path;
                            return m;
                        }));
                    });
            } else {

            }
        }

        public recommendations(callback: (data: MoviePresent[]) => void) {
            if (BackendService.MOCK) {
                this.$http.get("http://api.themoviedb.org/3/discover/movie?api_key=13ed7e5e07699386ba2c32a52aed7ae6")
                    .success(
                    (data: any) => {
                        callback(data.results.slice(0, 4).map(movie => {
                            var m = new dvdApp.Services.MoviePresent();
                            m.id = movie.id;
                            m.title = movie.original_title;
                            m.poster_path = "https://image.tmdb.org/t/p/w185" + movie.poster_path;
                            return m;
                        }));
                    });
            } else {

            }
        }

        public movieDetail(id: string, callback: (data: MovieDetail) => void) {
            if (BackendService.MOCK) {
                this.$http.get("http://api.themoviedb.org/3/movie/" + id + "?api_key=13ed7e5e07699386ba2c32a52aed7ae6&language=hu")
                    .success(
                    (data: any) => {
                        var m = new dvdApp.Services.MovieDetail();
                        m.id = data.id;
                        m.actors = ["actors"];
                        m.backdrop_path = "https://image.tmdb.org/t/p/original" + data.backdrop_path;
                        m.genres = data.genres.map((g) => { return g.name });
                        m.medium = "Cloud"
                        m.overview = data.overview;
                        m.poster_path = "https://image.tmdb.org/t/p/w185" + data.poster_path;
                        m.title = data.title;
                        m.trailer = "video";
                        m.year = data.release_date;

                        callback(m);
                    });
            } else {

            }
        }

        public media(callback: (data: string[]) => void): void {
            console.log("getting media");

            this.$http({
                method: "GET",
                url: BackendService.MEDIA_URI,
                headers: {
                    Authorization: 'Bearer ' + this.$auth.getToken()
                }
            }
            ).success(callback);
        }

        public searchFor(fragment: string, callback: (data: FragmentResult) => void): void {
            console.log("searching for fragment \"" + fragment + "\"");
            this.$http({
                method: "POST",
                url: BackendService.HELPER_SEARCH_URI,
                data: {
                    fragment: fragment
                },
                headers: {
                    Authorization: 'Bearer ' + this.$auth.getToken()
                }
            }
            ).success((data: any) => {
                if (data.results && data.first_result) {
                    var result: FragmentResult = new FragmentResult();

                    var first_result = new MovieDetail();
                    first_result.id = data.first_result.id;
                    first_result.title = data.first_result.title;
                    first_result.poster_path = data.first_result.poster_path;
                    first_result.overview = data.first_result.overview;
                    first_result.year = data.first_result.year;
                    first_result.genres = data.first_result.genres;
                    first_result.actors = data.first_result.actors;
                    first_result.trailer = data.first_result.trailer;
                    first_result.backdrop_path = data.first_result.backdrop_path;
                    first_result.medium = data.first_result.medium;

                    result.first_result = first_result;

                    result.results = data.results.map(pair => {
                        var m = new MovieBase();
                        m.id = pair.id;
                        m.title = pair.title;

                        return m;
                    });

                    callback(result);
                }
            });
        }
    }

    angular
        .module('dvdApp.Services', [])
        .service('BackendService', ['$http', '$q', '$auth', dvdApp.Services.BackendService]);

    export interface IBackendService {
        movies: (callback: (data: MoviePresent[]) => void) => void;
        recommendations: (callback: (data: MoviePresent[]) => void) => void;

        media: (callback: (data: string[]) => void) => void;
        searchFor: (fragment: string, callback: (data: FragmentResult) => void) => void;
    }

    export class FragmentResult {
        first_result: MoviePresent;
        results: MovieBase[];
    }

    export class MovieBase {
        id: string;
        title: string;
    }

    export class MoviePresent extends MovieBase {
        poster_path: string;
    }

    export class MovieDetail extends MoviePresent {
        overview: string;
        year: string;
        genres: string[];
        actors: string[];
        trailer: string;
        backdrop_path: string;
        medium: string;
    }
}
