'use strict';

angular.module('commentClient')
.controller('AdminSettingsCtrl',
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
    
    $scope.settings = restAPI.admin_extension.get();
    
    $scope.save = function() {
      $scope.settings.$save()
      .then(function(data){
        flash("Updated successfully!", false)
      })
      .catch(function(error){
        flash("Updating was failed!", true)
      })
    };
    
    $scope.jumpTo = function(route) {
      $location.path(route);
    };
    
    // function showErrorToast(error) {
    //   console.log($mdToast.simple())
    //   $mdToast.show(
    //     $mdToast.simple()
    //       .content(error)
    //       .position("top right")
    //       .hideDelay(3000)
    //   );
    // };
      
  }]);

  