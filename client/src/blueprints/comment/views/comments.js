'use strict';

angular.module('comment')
.controller('commentsCtrl', [
  '$http',
  'Config',
  '$scope', 
  'restAPI',
  '$location',
  "extManager",
  '$routeParams', 
  function(
    $http,
    Config,
    $scope, 
    restAPI,
    $location,
    extManager,
    $routeParams
  ) {
    
    $scope.group_id = $routeParams['group_id'];
    $scope.comments = restAPI.comment.query(
      {'group_id': $scope.group_id});
    
    $scope.selected = []
    $scope.toggle = function (item, list) {
      var idx = list.indexOf(item);
      if (idx > -1) list.splice(idx, 1);
      else list.push(item);
    };
    $scope.exists = function (item, list) {
      return list.indexOf(item) > -1;
    };
    $scope.disabled = function () {
      return !($scope.selected.length > 0);
    }
    
    $scope.removeBatchComment = function () {
      var comment_ids = []
      for (var i=0; i < $scope.selected.length; i++) {
        comment_ids.push($scope.selected[i].id)
      }
      
      var batch_comment = new restAPI.batch_comment({
        "group_id": $scope.group_id,
        "comment_ids": comment_ids
      });
      batch_comment.$batch_delete().then(function(data){
        for (var i=0; i < $scope.selected.length; i++) {
          $scope.comments.splice($scope.comments.indexOf(
            $scope.selected[i]), 1);
        }
        $scope.selected = []
        extManager.flash("Delete comments successfully!", false);
      });
    };
    
    $scope.removeComment = function (comment) {
      comment.$delete().then(function(data){
        $scope.comments.splice(comment, 1);
        extManager.flash("Delete comment successfully!", false);
      })
    };
    
    $scope.removeAllComment = function (){
      var comment_ids = []
      for (var i=0; i < $scope.comments.length; i++) {
        comment_ids.push($scope.comments[i].id)
      }
      
      var batch_comment = new restAPI.batch_comment({
        "group_id": $scope.group_id,
        "comment_ids": comment_ids
      });
      batch_comment.$batch_delete().then(function(data){
        for (var i=0; i < $scope.comments.length; i++) {
          $scope.comments.splice($scope.comments.indexOf(
            $scope.comments[i]), 1);
        }
        extManager.flash("Delete comments successfully!", false);
      });
    }
    
    
    
    $scope.jump_to = function(route) {
      $location.path(route);
    };
    
    
}]);