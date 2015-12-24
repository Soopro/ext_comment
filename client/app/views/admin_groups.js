'use strict';

angular.module('commentClient')
.controller('AdminGroupsCtrl',
[
  'flash',
  '$scope',
  'restAPI',
  '$location',
  function (
    flash,
    $scope,
    restAPI,
    $location
  ){
    
    $scope.groups = restAPI.admin_group.query();
    
    $scope.jumpTo = function(route) {
      $location.path(route);
    };
      
  }]);

  