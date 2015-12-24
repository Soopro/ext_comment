'use strict';

angular.module('commentClient')
.controller('AdminCommentsCtrl', [
  '$scope', 
  '$routeParams', 
  'restAPI',
  function(
    $scope, 
    $routeParams, 
    restAPI
  ) {
    
    $scope.group_id = $routeParams['group_id'];
    $scope.comments = restAPI.admin_comment.query({'group_id': $scope.group_id});
    
}]);