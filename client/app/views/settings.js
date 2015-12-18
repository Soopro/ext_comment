'use strict';

angular.module('commentClient')
.controller('SettingsCtrl',
[
  'flash',
  '$scope',
  'restAPI',
  function (
    flash,
    $scope,
    restAPI
  ){
    
    $scope.settings = restAPI.comment_extension.get();
    
    $scope.save = function() {
      $scope.settings.$save()
      .then(function(data){
        flash("Updated successfully!", false)
      })
      .catch(function(error){
        flash("Updating was failed!", true)
      })
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

  