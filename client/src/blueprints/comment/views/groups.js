'use strict';

angular.module('comment')
.controller('groupsCtrl',
[
  '$scope',
  'restAPI',
  '$location',
  function (
    $scope,
    restAPI,
    $location
  ){
    
    $scope.groups = restAPI.group.query();
    
    $scope.jump_to = function(route) {
      $location.path(route);
    };
      
  }]);

  