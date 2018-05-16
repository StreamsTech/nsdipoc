(function(){
    angular.module('layerApp').controller('layerVersionController',
    function($scope,layerService,uiGridConstants,$window){
        $scope.layerApprovalUrl="/api/layer-version-api/?layer_id=";
        $scope.versionSettingUrl="/api/change-layer-version-api/";
        $scope.layers=[];
        $scope.isDisable=false;
        $scope.postLayerId=undefined;
        angular.isUndefinedOrNull = function(val) {
            return angular.isUndefined(val) || val === null ;
        };
        function getAllLayerVersions(layerId){
            layerService.getLayerInformation($scope.layerApprovalUrl+layerId).then(function(response){
                $scope.layers=response.objects;
                $scope.isDisable=false;
                $scope.postLayerId=undefined;
            },function(error){
                console.log(error);
            });
        }

        $scope.inIt=function(layerId,currentVersion){
            getAllLayerVersions(layerId);
            $scope.layer_id=layerId;
            $scope.currentVersion=currentVersion;
        };
        $scope.setVersion=function(layer){
            var data={
                layer_id : $scope.layer_id,
                version_id : layer.id
            };
            $scope.postLayerId=layer.id;
            $scope.isDisable=true;
            layerService.setVersion($scope.versionSettingUrl,data).then(function(response){
                getAllLayerVersions($scope.layer_id);
                $scope.currentVersion=layer.version;
            },function(error){
                document.location.href="/layers/";
            });
        };
    });
})();