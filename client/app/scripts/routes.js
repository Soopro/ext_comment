'use strict';

/**
 * @ngdoc overview
 * @name commentClient
 * @description
 * # commentClient
 *
 * Main module of the application.
 */
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
      .when('/', {
        templateUrl: 'views/dashboard.html',
        controller: 'DashboardCtrl'
      })
      .when('/groups', {
        templateUrl: 'views/groups.html',
        controller: 'GroupsCtrl'
      })
      .when('/comments', {
        templateUrl: 'views/comments.html',
        controller: 'CommentsCtrl'
      })
      .when('/404', {
        templateUrl: 'views/404.html'
      })
      .otherwise({
        redirectTo: '/404'
      });
  }
]);
