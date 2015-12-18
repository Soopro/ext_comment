'use strict';

angular.module('commentClient')
.controller('CommentsCtrl', [
  '$scope', 
  '$routeParams', 
  'restAPI',
  function(
    $scope, 
    $routeParams, 
    restAPI
  ) {
    
    $scope.group_key = $routeParams.get('group_key')
    $scope.comments = restAPI.admin_group.get($scope.group_key)
  
}]);