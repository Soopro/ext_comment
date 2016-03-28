'use strict';

angular.module('comment')
.controller('settingsCtrl',
[
  '$scope',
  'restAPI',
  '$location',
  "extManager",
  function (
    $scope,
    restAPI,
    $location,
    extManager
  ){
    
    $scope.settings = restAPI.extension.get();
    
    $scope.save = function() {
      $scope.settings.$save()
      .then(function(data){
        extManager.flash("Updated successfully!", false)
      });
    };
    
    $scope.jump_to = function(route) {
      $location.path(route);
    };
      
  }]);

  