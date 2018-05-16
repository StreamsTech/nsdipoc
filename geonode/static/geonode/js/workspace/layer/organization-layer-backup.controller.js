/**
 * Created by rudra on 3/23/18.
 */
(function(){
    angular.module('layerApp').controller('organizationLayerBackupController',
    function($scope,layerService){
        $scope.backupUrl="/layers/organization/layers/backup";
        $scope.showLoader=false;
        $scope.success=false;
        $scope.error=false;
        $scope.message="An email has been sent to mail to download the backup files";
        $scope.backupLayer=function () {
            $scope.showLoader=true;
            layerService.backupOrganizationLayers($scope.backupUrl).then(function (response) {
                $scope.success=true;
                $scope.showLoader=false;
            },function (error) {
                $scope.message="Internal Server Error";
                $scope.error=true;
                $scope.showLoader=false;
            });

        }
    });
})();