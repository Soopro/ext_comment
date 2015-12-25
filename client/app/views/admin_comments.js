'use strict';

angular.module('commentClient')
.controller('AdminCommentsCtrl', [
  '$scope', 
  '$routeParams', 
  'restAPI',
  function(
    $scope, 
    $routeParams, 
    restAPI
  ) {
    
    $scope.group_id = $routeParams['group_id'];
    $scope.comments = restAPI.admin_comment.query({'group_id': $scope.group_id});
    
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
      // var ids = []
      // for (var i=0; i < $scope.selected.length; i++) {
      //   ids.push($scope.selected[i].id)
      //
      //   $http.post() //leave here
      //
      // }
      for (var i=0; i < $scope.selected.length; i++) {
        $scope.selected[i].delete({"comment_id": $scope.selected[i].id})
        .then(function(data){
          $scope.selected.splice($scope.selected.indexOf(data), 1);
          $scope.comments.splice($scope.comments.indexOf(data), 1);
          flash("Delete data successfully!", false);
        })
        .catch(function(error){
          flash("Delete data failed!", true);
        });
      }
    }
    
    
}]);