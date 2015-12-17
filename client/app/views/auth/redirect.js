'use strict';

/**
 * @ngdoc function
 * @name commentClient.controller:RedirectCtrl
 * @description
 * # RedirectCtrl
 * Controller of the commentClient
 */
angular.module('commentClient')
.controller('RedirectCtrl', function($routeParams, Auth, restAPI, $location) {
  if ($routeParams.code && $routeParams.state) {
    
    var params = {
      code: $routeParams.code,
      open_id: Auth.getOpenId(),
      state: $routeParams.state
    };

    restAPI.sup_auth.save({},params)
    .$promise
    .then(function (data) {
      Auth.setToken(data.ext_token);
      // Auth.setStatus(data.status);
      $location.url("/dashboard");
    })
  } else {
    alert("code and state is required!");
  }
});
