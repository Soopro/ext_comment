'use strict';

angular.module('commentClient')
.controller('GroupsCtrl',
[
  '$scope',
  'restAPI',
  function (
    $scope,
    restAPI
  ){
    
    $scope.groups = restAPI.list_comment_groups.query()
      
  }]);

  