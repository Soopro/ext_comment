/**
 * @ngdoc function
 * @name commentClient.controller:DashboardCtrl
 * @description
 * # DashboardCtrl
 * Controller of the commentClient
 */
angular.module('commentClient')
.controller('DashboardCtrl',['$cookies', function($scope, restAPI, Auth, $cookie, $location) {
  'use strict';

  var getCommentExtension = function () {
    var status = $cookie.get('status');
    if (status == 0) {
      restAPI.comment_extension.push();
    }
    else if (status == 1) {
      restAPI.comment_extension.get({open_id: open_id})
      .$promise
      .then(function (data) {
        $scope.comment_extension = data;
      })
      .catch(function (data) {
        console.error(data);
      });
    }
  };

  $scope.updateCommentExtension = function(comment_extension) {
    $scope.comment_extension.$save();
  };

  $scope.jumpToGroups = function() {
      $location.path('/groups');
  };

}]);