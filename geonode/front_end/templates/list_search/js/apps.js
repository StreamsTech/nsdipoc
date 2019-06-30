
(function(){
    'use strict';

angular
    .module('listSearchApp', [])
    .config(function($interpolateProvider) {
        // $httpProvider.defaults.withCredentials = true;
        $interpolateProvider.startSymbol('[{');
        $interpolateProvider.endSymbol('}]');

    });


})();