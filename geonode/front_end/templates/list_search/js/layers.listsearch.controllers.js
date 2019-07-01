(function () {
    'use strict';

    angular
        .module('listSearchApp')
        .controller('LayerListSearchController', function ($scope, $q, $window, $http, $timeout, dataListService) {
            var self = $scope;
            self.printme = "please convert me to angular js";
            self.searchString = "";
            self.resourceList = [];
            self.LAYER_LIST_API = "../api/list_search/layers-list";
            self.titleSearch = "";
            self.searchResults = [];

            self.organization = {
                selectedOrganization: null
            };
            self.category = {
                selectedCategory: null
            };

            self.setItems = function (url) {

                if (self.searchString) {
                    url += self.searchString;
                }
                self.resourceList = [];

                dataListService.getDataList(url).then(function (datalist) {
                    self.resourceList = datalist.data.results;
                    self.nextUrl = datalist.data.next;
                    self.previousUrl = datalist.data.previous;
                    self.counter = datalist.data.count;

                });

            };

            self.setSearchResults = function (url, searchString) {
                if (searchString) {
                    url += searchString;
                }
                self.searchResults = [];

                dataListService.getDataList(url).then(function (datalist) {
                    self.searchResults = datalist.data.results;
                });
            };

            self.getResourceList = function () {
                self.setItems(self.LAYER_LIST_API);
            };


            self.updateSearchString = function () {
                self.searchString = "";
                if (self.organization.selectedOrganization != null) {
                    self.searchString += "?group__slug=" + self.organization.selectedOrganization;
                }
                if (self.category.selectedCategory != null) {
                    if (self.searchString) {
                        self.searchString += "&category__gn_description=" + self.category.selectedCategory;
                    }
                    else {
                        self.searchString = "?category__gn_description=" + self.category.selectedCategory;
                    }

                }
                if (self.titleSearch) {
                    if (self.searchString) {
                        self.searchString += "&title__icontains=" + self.titleSearch;
                    }
                    else {
                        self.searchString = "?title__icontains=" + self.titleSearch;
                    }
                }
            };


            self.nextItems = function () {
                self.setItems(self.nextUrl);
            };
            self.previousItems = function () {
                self.setItems(self.previousUrl);
            };

            self.redirectTo = function (url, queryString) {
                $window.location.href = url + queryString;
            };

            self.loadOrganizationsList = function () {
                var url = '/api/groups/';

                dataListService.getDataList(url).then(function (datalist) {
                    self.organizations = datalist.data.objects;


                });
            };

            self.updateLayersWithTitle = function () {
                self.updateSearchString();
                self.setItems(self.LAYER_LIST_API);

            };

            self.updateLayersWithOrganization = function () {
                self.updateSearchString();
                self.setItems(self.LAYER_LIST_API);

            };


            self.loadCategoryList = function () {
                var url = '/api/categories/';

                dataListService.getDataList(url).then(function (datalist) {
                    self.categories = datalist.data.objects;


                });
            };

            self.updateLayersWithCategory = function () {
                self.updateSearchString();
                self.setItems(self.LAYER_LIST_API);

            };

            self.initdata = function () {
                self.loadOrganizationsList();
                self.loadCategoryList();
                self.getResourceList();

            };

            self.showSearchResults = function () {
                var message = document.getElementsByClassName('search-resource')[0];
                if (self.titleSearch)
                    message.style.display = 'block';
                else
                    self.hideSearchResults();
            };

            self.hideSearchResults = function () {
                var message = document.getElementsByClassName('search-resource')[0];
                message.style.display = 'none';

            };

            self.seaerchAutocomplete = function () {

                self.updateSearchString();
                self.setSearchResults(self.LAYER_LIST_API, self.searchString);
                self.showSearchResults();


            };


        })


})();