(function () {
    'use strict';

    var standardizationModule = angular
        .module('standardizationModule', ['angularFileUpload', 'ngCookies', 'surfToastr', 'ui.bootstrap'])
        .config(function ($interpolateProvider) {
            // $httpProvider.defaults.withCredentials = true;
            $interpolateProvider.startSymbol('[{');
            $interpolateProvider.endSymbol('}]');

        });

    standardizationModule.factory('standardizationService', ['$http', '$q', '$window', 'surfToastr',
        function ($http, $q, $window,surfToastr) {
            function get(url) {
                var deferred = $q.defer();
                $http.get(url)
                    .success(function (res) {
                        deferred.resolve(res);
                    }).error(function (error, status) {
                    deferred.reject({error: error, status: status});
                });
                return deferred.promise;
            }

            function put(url, obj) {
                var deferred = $q.defer();
                $http.put(url, obj, {
                    headers: {
                        "X-CSRFToken": $window.csrftoken
                    }
                }).success(function (res) {
                    deferred.resolve(res);
                }).error(function (error, status) {
                    deferred.reject({error: error, status: status});
                });
                return deferred.promise;
            }

            function post(url, obj) {
                var deferred = $q.defer();
                $http.post(url, obj, {
                    headers: {
                        "X-CSRFToken": $window.csrftoken
                    }
                }).success(function (res) {
                    surfToastr.success(res, 'Success');
                    deferred.resolve(res);
                }).error(function (error, status) {
                    surfToastr.success(error, 'Error!');
                    deferred.reject({error: error, status: status});
                });
                return deferred.promise;
            }

            function remove(url) {
                var deferred = $q.defer();
                $http.delete(url, {
                    headers: {
                        "X-CSRFToken": $cookies.get('csrftoken')
                    }
                })
                    .success(function (res) {
                        deferred.resolve(res);
                    }).error(function (error, status) {
                    deferred.reject({error: error, status: status});
                });
                return deferred.promise;
            }

            return {

                getData: function (url) {
                    return get(url);
                },

                updateData: function (ulr, data) {
                    return put(url, data);
                },

                postData: function (url, data) {
                    return post(url, data);
                },

                getYearMonth: function (year_month_obj) {

                    var year = year_month_obj.getFullYear();
                    var month = year_month_obj.getMonth() + 1;
                    if (month < 10)
                        month = '0' + month;
                    var year_month = year + '-' + month;
                    return year_month
                }
            };
        }
    ]);

    standardizationModule.controller('DPSController', [

        '$scope', 'FileUploader', '$window', 'surfToastr', 'standardizationService', '$modal',
        function ($scope, FileUploader, $window, surfToastr, modelDataUploadService, $modal) {

            $scope.init = function () {
                $scope.searchValue = null;
                $scope.next_url = null;
                $scope.previous_url = null;
                $scope.pageSize = 10;
                $scope.currentPage = 1;
                $scope.defaultSortField = "";

                $scope.data_api_url = '../../api/dps-list';
                get_data($scope.data_api_url);
            };

            function get_data(url) {
                modelDataUploadService.getData(url).then(function (data_list) {
                    $scope.report_data = data_list.results;
                    $scope.table_headers = data_list.report_table_headers;
                    $scope.next_url = data_list.next;
                    $scope.previous_url = data_list.previous;
                    $scope.totalPage = Math.ceil(data_list.count / $scope.pageSize);
                    if($scope.totalPage ==0){
                        $scope.currentPage = 0;
                    }
                });
            }

            $scope.filter_data = function () {
                $scope.currentPage = 1;
                if($scope.searchValue){
                    var query_string = 'search=' + $scope.searchValue.toString();
                    var filter_url = $scope.data_api_url + '?' + query_string;
                    get_data(filter_url);
                }
                else{
                    get_data($scope.data_api_url);
                }

            };

            $scope.orderData = function (orderValue){
                if(orderValue == $scope.defaultSortField){
                    $scope.defaultSortField = '-' + $scope.defaultSortField;
                }
                else {
                    $scope.defaultSortField = orderValue;
                }
                var filter_url = $scope.data_api_url + '?ordering=' + $scope.defaultSortField;
                get_data(filter_url);
            };

            $scope.next = function () {
                if($scope.next_url){
                    $scope.currentPage += 1;
                    get_data($scope.next_url);
                    }
            };

            $scope.previous = function () {
                if($scope.previous_url){
                    $scope.currentPage -= 1;
                    get_data($scope.previous_url);
                    }
            };

            $scope.showModal = function () {

                angular.element('#_delete_confirmation').modal('show')

            }

            $scope.hideModal = function () {

                angular.element('#_delete_confirmation').modal('hide')

            }

            $scope.downloadFile = function (url){
                $window.location.href = url;
            }

        }

    ]);

    standardizationModule.controller('WorkshopTrainingController', [

        '$scope', 'FileUploader', '$window', 'surfToastr', 'standardizationService', '$modal',
        function ($scope, FileUploader, $window, surfToastr, modelDataUploadService, $modal) {

            $scope.init = function () {
                $scope.searchValue = null;
                $scope.next_url = null;
                $scope.previous_url = null;
                $scope.pageSize = 10;
                $scope.currentPage = 1;
                $scope.defaultSortField = "";

                $scope.data_api_url = '../../api/dps-list';
                get_data($scope.data_api_url);
            };

            function get_data(url) {
                modelDataUploadService.getData(url).then(function (data_list) {
                    $scope.report_data = data_list.results;
                    $scope.table_headers = data_list.report_table_headers;
                    $scope.next_url = data_list.next;
                    $scope.previous_url = data_list.previous;
                    $scope.totalPage = Math.ceil(data_list.count / $scope.pageSize);
                    if($scope.totalPage ==0){
                        $scope.currentPage = 0;
                    }
                });
            }

            $scope.filter_data = function () {
                $scope.currentPage = 1;
                if($scope.searchValue){
                    var query_string = 'search=' + $scope.searchValue.toString();
                    var filter_url = $scope.data_api_url + '?' + query_string;
                    get_data(filter_url);
                }
                else{
                    get_data($scope.data_api_url);
                }

            };

            $scope.orderData = function (orderValue){
                if(orderValue == $scope.defaultSortField){
                    $scope.defaultSortField = '-' + $scope.defaultSortField;
                }
                else {
                    $scope.defaultSortField = orderValue;
                }
                var filter_url = $scope.data_api_url + '?ordering=' + $scope.defaultSortField;
                get_data(filter_url);
            };

            $scope.next = function () {
                if($scope.next_url){
                    $scope.currentPage += 1;
                    get_data($scope.next_url);
                    }
            };

            $scope.previous = function () {
                if($scope.previous_url){
                    $scope.currentPage -= 1;
                    get_data($scope.previous_url);
                    }
            };

            $scope.showModal = function () {

                angular.element('#_delete_confirmation').modal('show')

            }

            $scope.hideModal = function () {

                angular.element('#_delete_confirmation').modal('hide')

            }

            $scope.downloadFile = function (url){
                $window.location.href = url;
            }

        }

    ]);
    
})();