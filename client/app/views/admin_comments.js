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
    
    $scope.group_key = $routeParams['group_key'];
    $scope.comments = restAPI.admin_comment.query({'group_key': $scope.group_key});
    
}]);