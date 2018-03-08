(function(){
    angular.module('layerApp').controller('layerVersionController',
    function($scope,layerService,uiGridConstants,$window){
        $scope.layerApprovalUrl="/api/layer-version-api/?layer_id=";
        $scope.versionSettingUrl="/api/change-layer-version-api/";
        $scope.layers=[];
        angular.isUndefinedOrNull = function(val) {
            return angular.isUndefined(val) || val === null ;
        };
        function getAllLayerVersions(layerId){
            layerService.getLayerInformation($scope.layerApprovalUrl+layerId).then(function(response){
                $scope.layers=response.objects;
            },function(error){
                console.log(error);
            });
        }

        $scope.inIt=function(layerId){
            getAllLayerVersions(layerId);
            $scope.layer_id=layerId;
        };
        $scope.setVersion=function(layer){
            var data={
                layer_id : $scope.layer_id,
                version_id : layer.id
            };
            layerService.setVersion($scope.versionSettingUrl,data).then(function(response){
                $window.location.reload();
            });
        };
    });
})();