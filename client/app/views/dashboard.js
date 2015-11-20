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
  
    $scope.comment_extension = function () {
      var status = $cookie.get('status');
      if (status === 0) {
        restAPI.comment_extension.save({open_id: open_id});
      } else if (status == 1) {
        restAPI.comment_extension.get({open_id: open_id});
      }};
    
    $scope.comment_extension = function () {
      var status = $cookie.get('status');
      if (status == 0) {
        restAPI.comment_extension.save({open_id: open_id});
      } else if (status == 1) {
        restAPI.comment_extension.get({open_id: open_id})
      }
    };


    $scope.updateCommentExtension = function() {
      if (status == 1) {
        $scope.comment_extension.save();
      }
    };

    $scope.jumpToGroups = function() {
        $location.path('/groups');
    };

}]);