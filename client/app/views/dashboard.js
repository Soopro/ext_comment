'use strict';
/**
 * @ngdoc function
 * @name commentClient.controller:DashboardCtrl
 * @description
 * # DashboardCtrl
 * Controller of the commentClient
 */
angular.module('commentClient')
.controller('DashboardCtrl',
[
  '$scope',
  'restAPI',
  'Auth',  
  function (
    $scope,
    restAPI,
    Auth
  ){

    $scope.settings = restAPI.comment_extension.get()
    console.log($scope.settings)
      
    
}]);