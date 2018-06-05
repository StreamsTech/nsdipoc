(function(){
    angular.module('layerApp').controller('denyLayerController',
    function($scope,$modalInstance){
        $scope.deny={
            subject: undefined,
            comment: undefined,
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
    angular.module('layerApp').controller('approveLayerController',
    function($scope,layerService,uiGridConstants,$window,$q,$timeout,$modal){
        $scope.layer={};
        $scope.layer_id="";
        $scope.isAdmin=false;
        $scope.departments=[];
        $scope.gridApi={};
        $scope.isDisabledButton=false;
        $scope.layerApprovalUrl="/api/layer-attribute-permission-set/";
        $scope.gridOption = {
            enableRowSelection: true,
            enableSelectAll: true,
            rowHeight:30,
            data: [],
            enableGridMenu: false,
            exporterCsvFilename: self.layerName + '.csv',
            enableHorizontalScrollbar: uiGridConstants.scrollbars.ALWAYS,
            columnDefs: [
                { field: 'attribute' , displayName : 'Name'},
                { field: 'attribute_type',displayName : 'Data Type' },
                { name: 'id', visible: false,displayName:"Id" },
                { name: 'resource_uri', visible: false,displayName:"Resource Uri" }
            ]
        };
        $scope.gridOption.onRegisterApi = function(gridApi) {
            $scope.gridApi = gridApi;
          };

        function getPostLayerDataInformation(){
            var permissions = {
                'users': {},
                'groups': {}
              };
            permissions.users['AnonymousUser'] = [];
            var permissionAttributes=
          ['view_resourcebase', 'download_resourcebase'];
            var data={};
            data.layer_pk =$scope.layer_id;
            var permittedOrganizations=_.map(_.filter($scope.departments,function(department){
                return department.IsChecked;
                }),"slug");
            angular.forEach(permittedOrganizations,function(organizationId){
                permissions.groups[organizationId]= permissionAttributes;
            });
            data.permissions =permissions;//JSON.stringify(permissions);
            var selectedAttributes=_.map($scope.gridApi.selection.getSelectedRows(),"id");
            data.attributes =selectedAttributes;//JSON.stringify(selectedAttributes);
            return data;
        }

        function postLayerData(url,data){
            $scope.isDisabledButton=true;
            layerService.submitLayerInformation(url,data).then(function(response){
                document.location.href="/layers/";
                $scope.isDisabledButton=false;
            },function(error){
                $scope.isDisabledButton=false;
                console.log(error);
            });
        }


        $scope.submitforVerify=function(){
            var data=getPostLayerDataInformation();
            data.status="PENDING";
            postLayerData($scope.layerApprovalUrl,data);
        };

        $scope.verifyLayer=function(){
            var data=getPostLayerDataInformation();
            data.status="VERIFIED";
            postLayerData($scope.layerApprovalUrl,data);
        };
        $scope.approveLayer=function () {
            var data=getPostLayerDataInformation();
            data.status="ACTIVE";
            postLayerData($scope.layerApprovalUrl,data);
        };

        angular.isUndefinedOrNull = function(val) {
            return angular.isUndefined(val) || val === null ;
        };
        function getLayerInformation(layerId){
            layerService.getLayerInformation('/api/layer-attributes-permission/'+layerId+'/').then(function(response){
                $scope.layer=response;
                $scope.layer.access_level=response.limited_access ? 'Public' : 'Limited';
                $scope.layer.belongs_to="" + (angular.isUndefinedOrNull(response.sector) ? 'N/A' : response.sector) +' > '+
                                        (angular.isUndefinedOrNull(response.department) ? 'N/A' : response.department) +' > '+
                                        (angular.isUndefinedOrNull(response.organization) ? 'N/A' : response.organization ) +"";
                $scope.gridOption.data=response.attributes;
                $scope.gridApi.grid.modifyRows($scope.gridOption.data);
                var selectedAttribute=_.filter($scope.gridOption.data, function (attribute) {
                    return attribute.is_permitted;
                  });
                angular.forEach(selectedAttribute,function(attribute){
                    $scope.gridApi.selection.selectRow(attribute);
                });

              },function(error){
                  console.log(error);
            });
            $q.all({department: layerService.getOrganizations('/api/groups'), permissions: layerService.getLayerPermissions('/security/permissions/'+layerId)})
                    .then(function(resolutions){
                    var departments= resolutions.department.objects;
                    $scope.departments= _.object(_.map(departments, function(item) {
                        return [item.slug, item];
                     }));
                    var permissions  = Object.keys(JSON.parse(resolutions.permissions.permissions).groups);
                    angular.forEach(permissions,function(permission){
                        if($scope.departments[permission])
                            $scope.departments[permission].IsChecked=true;
                    });
                });
        }

        $scope.inIt=function(layerId,userRole){
            getLayerInformation(layerId);
            $scope.layer_id=layerId;
            $scope.userRole= (userRole == 'True' || userRole=='true');
        };
        $scope.openDenyModal=function () {
            $modal.open({
                templateUrl: 'denyModalContent.html',
                backdrop: 'static',
                keyboard: false,
                controller: 'denyLayerController'
            }).result.then(function(result) {
                var data = getPostLayerDataInformation();
                data.status = "DENIED";
                data.comment = result.comment;
                data.comment_subject= result.subject;
                postLayerData($scope.layerApprovalUrl, data);
            });
        }
    });
})();
