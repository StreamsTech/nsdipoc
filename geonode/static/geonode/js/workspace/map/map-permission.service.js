(function(){
    angular.module('mapPermissionApp')
    .service('mapPermissionService',function($http,$q){
         function get(url){
            var deferred = $q.defer();
            $http.get(url)
                .success(function (res) {
                    deferred.resolve(res);
                }).error(function (error, status) {
                deferred.reject({error: error, status: status});
            });
            return deferred.promise;
         }

         function post(url,data){
            var deferred = $q.defer();
            $http({
                url: url,
                method: "POST",
                data: data
                }).success(function (res) {
                    deferred.resolve(res);
                }).error(function (error, status) {
                deferred.reject({error: error, status: status});
            });
            return deferred.promise;
         }

        this.getMapInformation=function(url){
            return get(url);
        };
        this.submitMapInformation=function(url,data){
            return post(url,data);
        };
        this.publishMap=function(url,data){
            return post(url,data);
        };
        this.unPublishMap=function(url,data){
            return post(url,data);
        };
        this.getOrganizations=function(url){
            return get(url);
        };
        this.getMapPermissions=function(url){
            return get(url);
        };

    });
})();