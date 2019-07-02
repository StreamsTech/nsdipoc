
(function(){
    'use strict';

    angular
        .module('appModule')
        .service('categoryListService', function ($http, $q, $window) {
            function get(url) {
                var deferred = $q.defer();
                $http.get(url)
                    .then(function(res) {
                        deferred.resolve(res);
                    },function(error, status) {
                        deferred.reject({ error: error, status: status });
                    });
                return deferred.promise;
            }


            this.getDataList = function (url) {
                return get(url);
            };

            function post(url, obj) {
            var deferred = $q.defer();
            $http.put(url, obj, {
                headers: {
                    "X-CSRFToken": $window.csrf
                }
            }).success(function(res) {
                deferred.resolve(res);
            }).error(function(error, status) {
                deferred.reject({ error: error, status: status });
            });
            return deferred.promise;
        }



        });

})();
