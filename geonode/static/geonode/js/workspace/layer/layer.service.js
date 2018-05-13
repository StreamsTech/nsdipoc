(function(){
    angular.module('layerApp')
    .service('layerService',function($http,$q){

        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        var csrftoken = getCookie('csrftoken');


         function get(url){
            var deferred = $q.defer();
            $http.get(url,{ "X-CSRFToken" : csrftoken})
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

        this.getLayerInformation=function(url){
            return get(url);
        };
        this.submitLayerInformation=function(url,data){
            return post(url,data);
        };
        this.getAllLayers=function(url){
            return get(url);
        };
        this.publishLayer=function(url,data){
            return post(url,data);
        };
        this.unpublishLayer=function(url,data){
            return post(url,data);
        };
        this.getOrganizations=function(url){
            return get(url);
        };
        this.getAllLayerVersions=function(url){
            return get(url);
        };
        this.setVersion=function(url,data){
            return post(url,data);
        };
        this.getLayerPermissions=function(url){
            return get(url);  
        };
        this.backupOrganizationLayers=function (url) {
            return get(url);
        };

    });
})();