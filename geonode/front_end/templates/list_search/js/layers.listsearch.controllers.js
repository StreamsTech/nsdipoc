(function () {
    'use strict';

    angular
        .module('listSearchApp')
        .controller('ResourceListSearchController', function ($scope, $q, $window, $http, $timeout, dataListService) {
            var self = $scope;
            self.printme = "please convert me to angular js";
            self.searchString = "";
            self.resourceList = [];
            self.RESOURCE_LIST_API = "../api/list_search/resources-list";
            self.titleSearch = "";
            self.searchResults = [];
            self.resource_type = null;
            self.redirectUrl = null;
            self.nextUrl = null;
            self.previousUrl = null;
            self.currentUrl = null;
            self.organization = {
                selectedOrganization: null
            };
            self.category = {
                selectedCategory: null
            };

            self.orderby = {
                selectedOrderBy: '-date'
            };
            self.orders = [
                {option:'Most Recent', value:'-date'},
                {option:'Less Recent', value:'date'},
                {option:'A - Z', value:'title'},
                {option:'Z - A', value:'-title'},

            ];


            //----------------------------------------------------------------------------------------------------------
            self.getUrl = function (resource_type, organization, category, searchString) {
                var url;
                if (resource_type === 'layer')
                    url = self.RESOURCE_LIST_API + "?resource_type=layer";
                else if (resource_type === 'map')
                    url = self.RESOURCE_LIST_API + "?resource_type=map";
                else
                    url = self.RESOURCE_LIST_API + "?resource_type=document";

                if (organization)
                    url += "&group__slug=" + organization;
                if (category)
                    url += "&category__gn_description=" + category;
                if (searchString)
                    url += "&title__icontains=" + searchString;
                url += "&order_by=" + self.orderby.selectedOrderBy;
                return url;

            };

            self.setItems = function (url) {
                self.resourceList = [];
                dataListService.getDataList(url).then(function (datalist) {
                    self.resourceList = datalist.data.results;
                    self.nextUrl = datalist.data.next;
                    self.previousUrl = datalist.data.previous;
                    self.counter = datalist.data.count;
                });
            };

            self.setSearchItems = function (url, searchString) {
                if (searchString) {
                    url += searchString;
                }
                self.searchResults = [];

                dataListService.getDataList(url).then(function (datalist) {
                    self.searchResults = datalist.data.results;
                });
            };

            self.loadOrganizationsList = function () {
                var url = '/api/groups/';
                dataListService.getDataList(url).then(function (datalist) {
                    self.organizations = datalist.data.objects;
                });
            };

            self.loadCategoryList = function () {
                var url = '/api/categories/';

                dataListService.getDataList(url).then(function (datalist) {
                    self.categories = datalist.data.objects;
                });
            };

            self.updateResourceList = function () {
                self.setItems(self.getUrl(self.resource_type, self.organization.selectedOrganization, self.category.selectedCategory, null));
            };


            //----------------------------------------------------------------------------------------------------------
            self.showSearchResults = function () {
                var message = document.getElementsByClassName('search-resource')[0];
                if (self.searchString)
                    message.style.display = 'block';
                else
                    self.hideSearchResults();
            };

            self.hideSearchResults = function () {
                var message = document.getElementsByClassName('search-resource')[0];
                message.style.display = 'none';
            };

            self.searchAutocomplete = function () {
                if (self.searchString) {
                    self.setSearchItems(self.getUrl(self.resource_type, null, null, self.searchString));
                    self.showSearchResults();
                }
                else
                    self.hideSearchResults();

            };

            self.searchResources = function () {
                self.setItems(self.getUrl(self.resource_type, null, null, self.searchString));
            };


            //----------------------------------------------------------------------------------------------------------
            self.initdata = function (resource_type) {
                self.resource_type = resource_type;
                self.orderby.selectedOrderBy = '-date';
                self.loadOrganizationsList();
                self.loadCategoryList();
                self.setItems(self.getUrl(self.resource_type, null, null, null));
            };


            // ---------------------------------------------------------------------------------------------------------
            self.nextItems = function () {
                self.setItems(self.nextUrl);
            };
            self.previousItems = function () {
                self.setItems(self.previousUrl);
            };

            self.redirectTo = function (url) {
                $window.location.href = url;
            };


        })


})();