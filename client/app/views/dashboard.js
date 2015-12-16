'use strict';
/**
 * @ngdoc function
 * @name commentClient.controller:DashboardCtrl
 * @description
 * # DashboardCtrl
 * Controller of the commentClient
 */
angular.module('commentClient')
  .controller('DashboardCtrl', ['$cookies',
    function($scope, restAPI, Auth, $cookie, $location) {
      
      
      $scope.settings = restAPI.comment_extension.$get()
      
}]);