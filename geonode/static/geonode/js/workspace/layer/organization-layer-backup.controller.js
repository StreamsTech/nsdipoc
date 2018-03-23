/**
 * Created by rudra on 3/23/18.
 */
(function(){
    angular.module('layerApp').controller('organizationLayerBackupController',
    function($scope,layerService){
        $scope.backupUrl="/layers/organization/layers/backup";
        $scope.showLoader=false;
        $scope.message="An email has been sent to mail to download the backup files";
        $scope.backupLayer=function () {
            $scope.showLoader=true;
            layerService.backupOrganizationLayers($scope.backupUrl).then(function (response) {
                console.log(response);
            },function (error) {
                console.log(error);
            });

        }
    });
})();