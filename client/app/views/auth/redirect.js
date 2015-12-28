'use strict';

angular.module('commentClient')
.controller('RedirectCtrl', [
  '$routeParams', 
  'Auth', 
  'restAPI', 
  '$location',
  function(
    $routeParams, 
    Auth, 
    restAPI, 
    $location
  ) {
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
        $location.url("/admin/settings");
      })
      .catch(function (error) {
        console.log(error);
      })
    } else {
      alert("code and state is required!");
    }
}]);
