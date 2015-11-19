/**
 * @ngdoc function
 * @name commentClient.controller:CommentsCtrl
 * @description
 * # CommentsCtrl
 * Controller of the commentClient
 */

angular.module('commentClient')
.controller('CommentsCtrl', function($scope, $location, restAPI) {
  'use strict';
  $scope.comments = restAPI.group_comments.get()
  

  $scope.jumpToIndex = function() {
    $location.path('/');
  };
});
