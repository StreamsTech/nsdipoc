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
                $scope.searchedAccount = null;
                $scope.next_url = null;
                $scope.previous_url = null;
                $scope.pageSize = 10;
                $scope.currentPage = 1;

                $scope.data_api_url = '../../api/dps-list';
                get_report_data($scope.data_api_url);
            };

            function get_report_data(url) {
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
                var query_string = '';
                if($scope.selectedYearMonth){
                    var year = $scope.selectedYearMonth.getFullYear();
                    var month = $scope.selectedYearMonth.getMonth() + 1;
                    if (month < 10)
                        month = '0' + month;
                    query_string += 'year_month=' + year + '-' + month + '&';
                }
                if($scope.selectedDma){
                    query_string += 'dma_id=' + $scope.selectedDma.dma_id + '&'
                }
                if($scope.selectedZone){
                    query_string += 'zone_id=' + $scope.selectedZone.zone_id + '&'
                }
                if ($scope.searchedAccount){
                    query_string += 'account_id=' + $scope.searchedAccount + '&'
                }
                var filter_url = $scope.data_api_url + '?' + query_string;
                get_report_data(filter_url);

            };

            $scope.changeZone = function(){
                $scope.selectedDma = null;
                $scope.dmaListUnderZone = [];
                if ($scope.selectedZone){
                    var zone = $scope.selectedZone.zone_id;
                    $scope.dmaListUnderZone = $scope.report_filter_options.all_dma.filter(function(dma) { return dma.zone_id == zone });
                }
                $scope.filter_data();

            };

            $scope.next = function () {
                if($scope.next_url){
                    $scope.currentPage += 1;
                    get_report_data($scope.next_url);
                    }
            };

            $scope.previous = function () {
                if($scope.previous_url){
                    $scope.currentPage -= 1;
                    get_report_data($scope.previous_url);
                    }
            };

            $scope.deleteBulkmeterData = function (item) {


                console.log("ekhane aise")


                var itemId = item.id;
                var form_data = {
                        id: itemId
                };
                var bulk_dma_delete_api_url = '../../../../api/wasa/delete-bulk-meter-data';
                modelDataUploadService.postData(bulk_dma_delete_api_url, form_data).then(function (res) {
                    if(! res.error){
                        $scope.report_data.splice(itemId,1);
                        console.log($scope.report_data);
                        $scope.init('METER_READING');
                        $scope.hideModal()
                    }

                }).catch(function(err){
                    console.log(err)
                    $scope.hideModal()
                });


            }

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