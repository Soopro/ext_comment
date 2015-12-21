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
    $scope.newGroup = new restAPI.admin_group();
    
    $scope.jumpTo = function(route) {
      $location.path(route);
    };
    
    $scope.addCommentGroup = function() {
      if($scope.newGroup.group_key.lenth != 0) {
        $scope.newGroup.$save()
        .then(function(data){
          $scope.groups.push(data);
          flash("Add group successfully!", false)
        })
        .catch(function(error){
          flash("Failed! Try it again.", true)
        })
      }
    };
      
  }]);

  