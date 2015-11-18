/// <reference path="../../_all.ts" />
'use strict';

module dvdApp.Services {
    export class BackendService implements IBackendService {

        constructor(
            private $http: ng.IHttpService,
            private $q: ng.IQService,
            private $auth: any
        ) {
            this.$http = $http;
            this.$q = $q;
            this.$auth = $auth;
        }

        public media(callback: (data: string[]) => void) {
            console.log("getting media");

            this.$http({
                method: "GET",
                url: "http://localhost:5000/media",
                headers: {
                    Authorization: 'Bearer ' + this.$auth.getToken()
                }
            }
            ).success(callback);
        }

        public searchFor(fragment: string, callback: (data: { id: string, title: string }[]) => void) {
            console.log("searching for fragment \""+ fragment +"\"");
            this.$http({
                method: "POST",
                url: "http://127.0.0.1:5000/helper/search",
                data: {
                    fragment: fragment
                },
                headers: {
                    Authorization: 'Bearer ' + this.$auth.getToken()
                }
            }
            ).success((data: any) => {
                if (data.possible_ids) {
                                        
                    var pairs = data.possible_ids.map(
                        (value, index) => {
                            return {
                                id: value,
                                title: (<any>data).possible_titles[index]
                            }
                        });

                    callback(pairs);
                }
            });
        }



    }

    angular
        .module('dvdApp.Services', [])
        .service('BackendService', ['$http', '$q', '$auth', dvdApp.Services.BackendService]);

    export interface IBackendService {
        media: (callback: ng.IHttpPromiseCallback<string[]>) => void;
        searchFor: (fragment: string, callback: ng.IHttpPromiseCallback<{ id: string, title: string }[]>) =>void;
    }
}
