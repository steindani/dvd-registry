/// <reference path="../../_all.ts" />
'use strict';

module dvdApp.Services {
    export class BackendService implements IBackendService {

        private static MEDIA_URI: string = "http://localhost:5000/media";
        private static HELPER_SEARCH_URI: string = "http://127.0.0.1:5000/helper/search";
        private static ADD_MOVIE_URI: string = "http://127.0.0.1:5000/movies";
        private static GET_MOVIES_URI: string = "http://127.0.0.1:5000/movies";
        private static GET_MOVIE_DETAILS_URI: string = "http://127.0.0.1:5000/movie/";
        private static RECOMMENDATION_URI: string = "http://127.0.0.1:5000/random";
        private static SEARCH_URI: string = "http://127.0.0.1:5000/search/movies ";


        private static MOCK = false;

        constructor(
            private $http: ng.IHttpService,
            private $q: ng.IQService,
            private $auth: any
        ) {
            this.$http = $http;
            this.$q = $q;
            this.$auth = $auth;
        }

        public filterResults: string[] = null;
        public updateFilter(query: string) {
            if (query === "") {
                this.filterResults = null;
                return;
            }
            
            this.$http({
                method: "POST",
                url: BackendService.SEARCH_URI,
                data: { criteria: query },
                headers: {
                    Authorization: 'Bearer ' + this.$auth.getToken()
                }
            }).success((data: any) => {
                this.filterResults = data.movies;
            });
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
                this.$http({
                    method: "GET",
                    url: BackendService.GET_MOVIES_URI,
                    headers: {
                        Authorization: 'Bearer ' + this.$auth.getToken()
                    }
                }
                ).success((data: any) => {
                    callback(
                        data.movies.map(movie => {
                            return {
                                id: movie.movie_id,
                                poster_path: movie.cover,
                                title: movie.title,
                                year: movie.year
                            }
                        }));
                });
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
                this.$http({
                    method: "GET",
                    url: BackendService.RECOMMENDATION_URI,
                    headers: {
                        Authorization: 'Bearer ' + this.$auth.getToken()
                    }
                }
                ).success((data: any) => {
                    callback(
                        data.movies.map(movie => {
                            return {
                                id: movie.movie_id,
                                poster_path: movie.cover,
                                title: movie.title,
                                year: movie.year
                            }
                        }));
                });
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
                this.$http({
                    method: "GET",
                    url: BackendService.GET_MOVIE_DETAILS_URI + id,
                    headers: {
                        Authorization: 'Bearer ' + this.$auth.getToken()
                    }
                }
                ).success((data: any) => {
                    var m = new dvdApp.Services.MovieDetail();
                    m.id = data.id;
                    m.actors = data.actors;
                    m.backdrop_path = data.backdrop_path;
                    m.genres = data.genres;
                    m.medium = data.medium;
                    m.overview = data.plot;
                    m.title = data.title;
                    m.trailer = data.trailer;
                    m.year = data.year;

                    callback(m);
                });
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

        public addMovie(id: string, title: string, media: string, callback: (data: any) => void): void {
            console.log("adding new movie: " + id + " " + title + " " + media);

            var data: any = {};
            if (id) {
                data.id = id;
            }
            if (title) {
                data.title = title;
            }
            if (media) {
                data.media = media;
            }
            
            // TODO feedback on empty media

            this.$http({
                method: "POST",
                url: BackendService.ADD_MOVIE_URI,
                data: data,
                headers: {
                    Authorization: 'Bearer ' + this.$auth.getToken()
                }
            }).success((data: any) => {
                callback({
                    id: data.movie_id,
                    poster_path: data.cover,
                    title: data.title,
                    year: data.year
                })
            });
        }
    }

    angular
        .module('dvdApp.Services', [])
        .service('BackendService', ['$http', '$q', '$auth', dvdApp.Services.BackendService]);

    export interface IBackendService {
        movies: (callback: (data: MoviePresent[]) => void) => void;
        recommendations: (callback: (data: MoviePresent[]) => void) => void;
        filterResults: string[];

        media: (callback: (data: string[]) => void) => void;
        searchFor: (fragment: string, callback: (data: FragmentResult) => void) => void;

        addMovie: (id: string, title: string, media: string, callback: (data: any) => void) => void;
        updateFilter: (query: string) => void;
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
        year: string;
    }

    export class MovieDetail extends MoviePresent {
        overview: string;
        genres: string[];
        actors: string[];
        trailer: string;
        backdrop_path: string;
        medium: string;
    }
}
