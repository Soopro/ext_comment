'use strict';

angular.module('commentClient')
.controller('AdminGenerateCodeCtrl',
[
  '$scope',
  function (
    $scope
  ){
    
    $scope.group_key = ''
    $scope.code = ''
    
    $scope.generateCode = function(){
      $scope.code = $scope.group_key
    }
      
  }]);