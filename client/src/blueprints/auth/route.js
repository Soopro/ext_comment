angular.module('comment')

.config([
  '$routeProvider',

  function(
    $routeProvider
  ){
    'use strict';
  
    var bp = "auth"
    var dir = "blueprints/auth/views"

    $routeProvider
    .when('/'+bp, {
      template: '',
      controller: 'authCtrl'
    })
    .when('/'+bp+'/redirect', {
      template: '',
      controller: 'authRedirectCtrl'
    })
  }
])