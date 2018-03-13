(function(){
    angular.module('mapPermissionApp').controller('approveMapController',
    function($scope,mapPermissionService,uiGridConstants,$window,$q,$timeout){
        $scope.mapId="";
        $scope.isAdmin=false;
        $scope.departments=[];
        $scope.layerApprovalUrl="/api/resource-attribute-permission-set/";

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
            var permittedOrganizations=_.map(_.filter($scope.departments,function(department){
                return department.IsChecked;
                }),"slug");
            angular.forEach(permittedOrganizations,function(organizationId){
                permissions.groups[organizationId]= permissionAttributes;
            });
            data.permissions =permissions;//JSON.stringify(permissions);

            return data;
        }

        function postLayerData(url,data){
            $scope.isDisabledButton=true;
            mapPermissionService.submitMapInformation(url,data).then(function(response){
                document.location.href="/maps/";
                $scope.isDisabledButton=false;
            },function(error){
                $scope.isDisabledButton=false;
                console.log(error);
            });
        }


        $scope.approveLayer=function(){
            var data=getPostLayerDataInformation();
            data.status="PENDING";
            console.log(data);
            postLayerData($scope.layerApprovalUrl,data);
        };

        $scope.publishLayer=function(){
            var data=getPostLayerDataInformation();
            data.status="ACTIVE";
            console.log(data);
            postLayerData($scope.layerApprovalUrl,data);
        };
        angular.isUndefinedOrNull = function(val) {
            return angular.isUndefined(val) || val === null ;
        };
        function getLayerInformation(layerId){
           mapPermissionService.getOrganizations('/api/groups')
                    .then(function(response){
                    var departments= response.objects;
                    $scope.departments= _.object(_.map(departments, function(item) {
                        return [item.slug, item];
                     }));
                });
        }

        $scope.inIt=function(mapId,userRole){
            getLayerInformation('');
            $scope.mapId=mapId;
            $scope.userRole= (userRole == 'True' || userRole=='true');
        };
    });
})();