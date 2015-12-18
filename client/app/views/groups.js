'use strict';

angular.module('commentClient')
.controller('GroupsCtrl',
[
  '$scope',
  'restAPI',
  '$location',
  function (
    $scope,
    restAPI,
    $location
  ){
    
    $scope.groups = restAPI.admin_groups.query()
      
  }]);

  