(function(){
    angular.module('documentPermissionApp').controller('denyDocumentController',
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
    angular.module('documentPermissionApp').controller('approveDocumentController',
    function($scope,documentPermissionService,uiGridConstants,$window,$q,$timeout,$modal){
        $scope.documentId="";
        $scope.isAdmin=false;
        $scope.departments=[];
        $scope.denyLoader = false;
        $scope.isDisabledButton = false;
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
            data.resource_pk =$scope.documentId;
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
            documentPermissionService.submitDocumentInformation(url,data).then(function(response){
                document.location.href="/documents/";
            },function(error){
                $scope.isDisabledButton=false;
                console.log(error);
            });
        }

        $scope.submitforVerify=function(){
            var data=getPostLayerDataInformation();
            data.status="PENDING";
            $scope.isDisabledButton=true;
            postLayerData($scope.layerApprovalUrl,data);
        };

        $scope.verifyDocument=function(){
            var data=getPostLayerDataInformation();
            data.status="VERIFIED";
            $scope.isDisabledButton=true;
            postLayerData($scope.layerApprovalUrl,data);
        };
        $scope.approveDocument=function () {
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
                department: documentPermissionService.getOrganizations('/api/groups'),
                permissions: documentPermissionService.getDocumentPermissions('/security/permissions/' + layerId)
            }).then(function (resolutions) {
                var departments = resolutions.department.objects;
                $scope.departments = _.object(_.map(departments, function (item) {
                    return [item.slug, item];
                }));
                var permissions = Object.keys(JSON.parse(resolutions.permissions.permissions).groups);
                angular.forEach(permissions, function (permission) {
                    if ($scope.departments[permission])
                        $scope.departments[permission].IsChecked = true;
                });
            });
        }

        $scope.inIt=function(documentId,userRole){
            getLayerInformation(documentId);
            $scope.documentId=documentId;
            $scope.userRole= (userRole == 'True' || userRole=='true');
        };

        $scope.openDenyModal = function () {
            $modal.open({
                templateUrl: 'denyModalContent.html',
                backdrop: 'static',
                keyboard: false,
                controller: 'denyDocumentController'
            }).result.then(function (result) {
                var data = getPostLayerDataInformation();
                data.status = "DENIED";
                data.comment = result.comment;
                data.comment_subject = result.subject;
                $scope.denyLoader = true;
                postLayerData($scope.layerApprovalUrl, data);
            });
        }
    });
})();