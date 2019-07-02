appModule.controller('catalogBrowserController', catalogBrowserController);
catalogBrowserController.$inject = ['$scope',
    '$http',
    '$rootScope',
    'surfToastr',
    'mapService',
    'layerService',
    'categoryListService',
    '$modalInstance'
];

function catalogBrowserController($scope, $http, $rootScope, surfToastr, mapService, layerService, categoryListService, $modalInstance) {

    $scope.serverList = [{
            name: 'Geoserver',
            method: loadLayersByApi
        },
        // {
        //     name: 'geodata.nationaalgeoregister',
        //     url: 'https://geodata.nationaalgeoregister.nl/bestuurlijkegrenzen/wms',
        //     type: 'wms',
        //     method: loadLayersByWms

        // }
    ];

    $scope.organization = {
        selectedOrganization:null
    };
    $scope.category = {
        selectedCategory:null
    };

    function loadLayersByWms(server) {
        var url = server.url + '?service=wms&tiled=true&request=GetCapabilities&access_token=9df608bcabe911e7a833080027252357';
        layerService.fetchWmsLayers(url)
            .then(function(res) {
                $scope.layers = res;
                $scope.layers.forEach(function(e) {
                    e.geoserverUrl = server.url;
                }, this);
            });
    }

    function loadLayersByApi(server, group, category) {
        layerService.fetchLayers(group, category)
            .then(function(res) {
                $scope.layers = res;
            });
    }
    $scope.loadLayers = function(server) {
        $scope.selectedServerName = server.name;
        server.method(server, $scope.organization.selectedOrganization, $scope.category.selectedCategory);

    };

    $scope.addLayer = function(layer) {
        let newlayer = Object.assign({}, layer, { SortOrder: mapService.sortableLayers.length + 1 });
        mapService.addDataLayer(newlayer)
            .then(function(res) {               
                surfToastr.success('Layer Added to The Map Successfully.', 'Success');
            }, function(res){
                surfToastr.success('Layer Add Failed', 'Error!!!');
            });
    };

    $scope.closeDialog = function() {
        $modalInstance.close();
    };

    $scope.initdata = function(){
        $scope.loadCategoryList();
        $scope.loadOrganizationsList();
        $scope.organization.selectedOrganization = null;
        $scope.category.selectedCategory = null;
        $scope.loadLayers($scope.serverList[0])
    };

    $scope.loadCategoryList = function(){
        var url = '/api/categories/';

        categoryListService.getDataList(url).then(function (datalist) {
            $scope.categories = datalist.data.objects;


        });
    };

    $scope.loadOrganizationsList = function(){
        var url = '/api/groups/';

        categoryListService.getDataList(url).then(function (datalist) {
            $scope.organizations = datalist.data.objects;


        });
    };

    $scope.updateLayersWithOrganization = function () {
        $scope.loadLayers($scope.serverList[0])

    };
    $scope.updateLayersWithCategory = function () {
        $scope.loadLayers($scope.serverList[0])

    }

}