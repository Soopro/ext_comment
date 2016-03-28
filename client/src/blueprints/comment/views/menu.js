angular.module('comment')

.controller('menuCtrl', [
  '$scope',
  '$location',
  'Config',
  'extManager',
  
  function(
    $scope,
    $location,
    Config, 
    extManager
  ){
    'use strict'
    $scope.is_list = $location.path() == Config.route.portal
    
    $scope.return = function() {
      $location.path(Config.route.portal)
    }
    
    $scope.close = function() {
      extManager.close()
    }
    
    $scope.jump_to = function(route){
      $location.path(route);
    };
  }
])
