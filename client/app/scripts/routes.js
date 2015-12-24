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
      .when('/admin/settings', {
        templateUrl: 'views/admin_settings.html',
        controller: 'AdminSettingsCtrl'
      })
      .when('/admin/generation', {
        templateUrl: 'views/admin_generate_code.html',
        controller: 'AdminGenerateCodeCtrl'
      })
      .when('/admin/group', {
        templateUrl: 'views/admin_groups.html',
        controller: 'AdminGroupsCtrl'
      })
      .when('/admin/group/:group_id/comment', {
        templateUrl: 'views/admin_comments.html',
        controller: 'AdminCommentsCtrl'
      })
      .when('/visit/group/:group_key/comment', {
        templateUrl: 'views/visit_comments.html',
        controller: 'VisitCommentsCtrl'
      })
      .when('/404', {
        templateUrl: 'views/404.html'
      })
      .otherwise({
        redirectTo: '/404'
      });
  }
]);
