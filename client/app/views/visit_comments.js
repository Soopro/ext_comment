'use strict';

angular.module('commentClient')
.controller('VisitCommentsCtrl', [
  'flash',
  '$scope', 
  '$routeParams', 
  'restAPI',
  function(
    flash,
    $scope, 
    $routeParams, 
    restAPI
  ) {
    
    $scope.group_key = $routeParams['group_key'];
    $scope.comments = restAPI.visit_comment.query(
      {'group_key': $scope.group_key});
    $scope.newComment = new restAPI.visit_comment();
    $scope.addComment = function(){
      $scope.newComment.$save({'group_key': $scope.group_key})
      .then(function(data){
        $scope.comments.push(data);
        flash("Commented successfully!", false);
        $scope.newComment = new restAPI.visit_comment();
      })
      .catch(function(error){
        flash("Submitting was failed! ", true);
      });
    };
    
}]);