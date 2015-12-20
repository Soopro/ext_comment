'use strict';

angular.module('commentClient')
.config([
  "$routeProvider",
  function ($routeProvider) {
    $routeProvider
      .when('/auth', {
        templateUrl: 'views/auth/auth.html',
        controller: 'AuthCtrl'
      })
      .when('/redirect', {
        templateUrl: 'views/auth/redirect.html',
        controller: 'RedirectCtrl'
      })
      .when('/settings', {
        templateUrl: 'views/settings.html',
        controller: 'SettingsCtrl'
      })
      .when('/groups', {
        templateUrl: 'views/groups.html',
        controller: 'GroupsCtrl'
      })
      .when('/group/:group_key', {
        templateUrl: 'views/group.html',
        controller: 'GroupCtrl'
      })
      .when('/404', {
        templateUrl: 'views/404.html'
      })
      .otherwise({
        redirectTo: '/404'
      });
  }
]);
