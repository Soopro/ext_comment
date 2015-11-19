/**
 * @ngdoc function
 * @name commentClient.controller:DashboardCtrl
 * @description
 * # GroupsCtrl
 * Controller of the commentClient
 */

angular.module('commentClient')
  .controller('GroupsCtrl', function($scope, $location) {
    'use strict';
    $scope.groups = [{
      group_key: 'Group Name one',
      creation: 'Min Li Chan',
    }, {
      group_key: 'Group Name second',
      creation: 'Min Li Chan',
    }, {
      group_key: 'Group Name 4',
      creation: 'Min Li Chan',
    }, {
      group_key: 'Group Name 5',
      creation: 'Min Li Chan',
    }, {
      group_key: 'Group Name 6',
      creation: 'Min Li Chan',
    }];

    $scope.jumpToIndex = function() {
      $location.path('/');
    };
});
