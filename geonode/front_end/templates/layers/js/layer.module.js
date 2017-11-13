(function() {
    angular.module('LayerApp', ['ui.grid', 'ui.grid.pagination', 'ui.grid.exporter'])
        .config(['$interpolateProvider', '$locationProvider', function($interpolateProvider, $locationProvider) {
            $interpolateProvider.startSymbol('[{');
            $interpolateProvider.endSymbol('}]');
            $locationProvider.html5Mode(true);
        }]);
})();