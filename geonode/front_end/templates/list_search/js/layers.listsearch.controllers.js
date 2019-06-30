
(function(){
    'use strict';

angular
    .module('listSearchApp')
    .controller('LayerListSearchController', function ($scope, $q, $window, $http, $timeout, dataListService) {
        var self = $scope;
    self.printme = "please convert me to angular js";
    self.searchString = null;
    self.currentTab = 0;
    self.resourceList = null;
    self.layerListApiUrl = "../api/list_search/layers-list";



    self.setItems = function(url){

        if(self.searchString){
            url +=  self.searchString;
        }
        self.resourceList = [];
        self.checkAll = false;
        self.selectedItems = [];

        dataListService.getDataList(url).then(function (datalist) {
            self.resourceList = datalist.data.results;
            self.nextUrl = datalist.data.next;
            self.previousUrl = datalist.data.previous;
            self.counter = datalist.data.offset;
            self.results = self.resourceList;

        });

    };


        self.getResourceList = function (){
            self.currentTab = 1;
            self.searchString = null;
            self.setItems(self.layerListApiUrl);
        };


        self.nextItems = function(){
            self.setItems(self.nextUrl);
        };
        self.previousItems = function(){
            self.setItems(self.previousUrl);
        };

        self.redirectTo = function(url, queryString){
            $window.location.href = url+queryString;
        };


    self.getResourceList();


})



})();