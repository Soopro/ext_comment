'use strict';

angular.module('commentClient')
.controller('GroupCtrl', [
  '$scope', 
  '$routeParams', 
  'restAPI',
  function(
    $scope, 
    $routeParams, 
    restAPI
  ) {
    
    $scope.group_key = $routeParams.get('group_key')
    $scope.comments = restAPI.admin_group.query($scope.group_key)
  
}]);