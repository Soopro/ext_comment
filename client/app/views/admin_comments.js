'use strict';

angular.module('commentClient')
.controller('AdminCommentsCtrl', [
  'flash',
  '$http',
  'Config',
  '$scope', 
  'restAPI',
  '$location',
  '$routeParams', 
  function(
    flash,
    $http,
    Config,
    $scope, 
    restAPI,
    $location,
    $routeParams
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
      var ids = []
      for (var i=0; i < $scope.selected.length; i++) {
        ids.push($scope.selected[i].id)
      }
      var data = {"ids": ids};
      $http.post(Config.api + "/admin/group/" + 
        $scope.group_id + "/comment/batch", data)
      .success(function (data) {
        for (var i=0; i < $scope.selected.length; i++) {
          $scope.comments.splice($scope.comments.indexOf(
            $scope.selected[i]), 1);
        }
        $scope.selected = []
        flash("Delete data successfully!", false);
      })
      .error(function (error) {
        flash("Delete data failed!", true);
      });
      //
      // for (var i=0; i < $scope.selected.length; i++) {
      //   $scope.selected[i].delete({"comment_id": $scope.selected[i].id})
      //   .then(function(data){
      //     $scope.selected.splice($scope.selected.indexOf(data), 1);
      //     $scope.comments.splice($scope.comments.indexOf(data), 1);
      //     flash("Delete data successfully!", false);
      //   })
      //   .catch(function(error){
      //     flash("Delete data failed!", true);
      //   });
      // }
    }
    
    $scope.jumpTo = function(route) {
      $location.path(route);
    };
    
    
}]);