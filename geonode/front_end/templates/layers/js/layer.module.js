(function() {
    angular.module('LayerApp', ['ngCookies','ui.grid', 'ui.grid.pagination', 'ui.grid.exporter', 'angularFileUpload'])
        .config(['$interpolateProvider', '$locationProvider', function($interpolateProvider, $locationProvider) {
            $interpolateProvider.startSymbol('[{');
            $interpolateProvider.endSymbol('}]');
            $locationProvider.html5Mode(true);
        }])
        .run(['$http', '$cookies', function($http, $cookies) {
            $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
          }])
        .factory('AngularUiGridOptions', ['uiGridConstants', function(uiGridConstants) {
            return function() {
                this.paginationPageSizes = [25, 50, 75, 100];
                this.paginationPageSize = 25;
                this.data = [];
                this.minRowsToShow = 15;
                this.enableGridMenu = true;
                this.exporterCsvFilename = 'data.csv';
                this.enableHorizontalScrollbar = uiGridConstants.scrollbars.ALWAYS;
            }
        }]);
})();