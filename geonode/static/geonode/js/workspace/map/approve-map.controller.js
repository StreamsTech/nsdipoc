(function(){
    angular.module('mapPermissionApp').controller('denyMapController',
    function($scope,$modalInstance){
        $scope.deny={
            subject: undefined,
            comment: undefined
        };
        $scope.ok=function () {
            if($scope.deny.subject && $scope.deny.comment){
                $modalInstance.close($scope.deny);
            }
        };

        $scope.cancel=function () {
            $modalInstance.dismiss('cancel');
        }
    });
})();
(function(){
    angular.module('mapPermissionApp').controller('approveMapController',
    function($scope,mapPermissionService,$modal,$q){
        $scope.mapId="";
        $scope.isAdmin=false;
        $scope.departments=[];
        $scope.denyLoader=false;
        $scope.isDisabledButton = false;
        $scope.layerApprovalUrl="/api/map-attribute-permission-set/";

        function getPostLayerDataInformation(){
            var permissions = {
                'users': {},
                'groups': {}
              };
            permissions.users['AnonymousUser'] = [];
            var permissionAttributes=
          ['view_resourcebase', 'download_resourcebase'];
            var data={};
            data.resource_pk =$scope.mapId;
            var permittedOrganizations= getSelectedOrganizations();
            angular.forEach(permittedOrganizations,function(organizationId){
                permissions.groups[organizationId]= permissionAttributes;
            });
            data.permissions =permissions;//JSON.stringify(permissions);

            return data;
        }

        function postLayerData(url,data){
            mapPermissionService.submitMapInformation(url,data).then(function(response){
                document.location.href="/maps/";
                $scope.isDisabledButton=false;
                $scope.denyLoader = false;
            },function(error){
                $scope.isDisabledButton=false;
                $scope.denyLoader = false;
                console.log(error);
            });
        }


        $scope.submitforVerify=function(){
            var data=getPostLayerDataInformation();
            data.status="PENDING";
            $scope.isDisabledButton=true;
            postLayerData($scope.layerApprovalUrl,data);
        };

        $scope.verifyLayer=function(){
            var data=getPostLayerDataInformation();
            data.status="VERIFIED";
            $scope.isDisabledButton=true;
            postLayerData($scope.layerApprovalUrl,data);
        };
        $scope.approveLayer=function () {
            var data=getPostLayerDataInformation();
            data.status="ACTIVE";
            $scope.isDisabledButton=true;
            postLayerData($scope.layerApprovalUrl,data);
        };

        angular.isUndefinedOrNull = function(val) {
            return angular.isUndefined(val) || val === null ;
        };
        function getLayerInformation(layerId){
            $q.all({
                permissions: mapPermissionService.getMapPermissions('/security/permissions/' + layerId)
            })
                .then(function (resolutions) {
                    var permissions = Object.keys(JSON.parse(resolutions.permissions.permissions).groups);
                    $(document).ready(function () {
                            getOrganizationData(permissions);
                        });
                });
        }

        $scope.inIt=function(mapId,userRole){
            $scope.mapId=mapId;
            getLayerInformation(mapId);
            $scope.userRole= (userRole == 'True' || userRole=='true');
        };
        $scope.openDenyModal=function () {
            $modal.open({
                templateUrl: 'denyModalContent.html',
                backdrop: 'static',
                keyboard: false,
                controller: 'denyMapController'
            }).result.then(function(result) {
                var data = getPostLayerDataInformation();
                data.status = "DENIED";
                data.comment = result.comment;
                data.comment_subject= result.subject;
                $scope.denyLoader=true;
                postLayerData($scope.layerApprovalUrl, data);
            });
        }
    });
})();