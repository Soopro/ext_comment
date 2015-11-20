/**
 * @ngdoc function
 * @name commentClient.controller:CommentsCtrl
 * @description
 * # CommentsCtrl
 * Controller of the commentClient
 */

angular.module('commentClient')
.controller('CommentsCtrl', function($scope, $location, $routeParams, restAPI) {
  'use strict';
  $scope.comments = restAPI.group_comments.get();
  
  $scope.jumpToIndex = function() {
    $location.path('/');
  };

  $scope.adminRemoveComment = function() {
    if ($routeParams.group_key && $routeParams.comment_id) {
      var group_key = $routeParams.group_key;
      var comment_id = $routeParams.comment_id;
      return restAPI.admin_remove_comment.delete({group_key: group_key,
                                         comment_id: comment_id});
    } else {
      alert('group_key and commment_id are required!');
    };
  }

  $scope.outerRemoveComment = function() {
    if ($routeParams.group_key && $routeParams.comment_id) {
      var group_key = $routeParams.group_key;
      var comment_id = $routeParams.comment_id;
      return restAPI.remove_comment.delete({group_key: group_key,
                                         comment_id: comment_id});
    } else {
      alert('group_key and commment_id are required!');
    };
  };
};
});