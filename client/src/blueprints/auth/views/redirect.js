angular.module('comment')

.controller('authRedirectCtrl', [
  '$routeParams',
  '$location',
  'Auth',
  'restUser',
  'Config',

  function(
    $routeParams,
    $location,
    Auth,
    restUser,
    Config
  ){
    'use strict';

    if ($routeParams.code && $routeParams.state) {

      var params = {
        code: $routeParams.code,
        open_id: Auth.get_open_id(),
        state: $routeParams.state
      }
      var auth = new restUser.auth(params)
      
      auth.$access()
      .then(function (data) {
        Auth.set_token(data.token)
        $location.path(Config.route.portal)
      })
    } else {
      console.error("code and state is required!")
      $location.path(Config.route.error)
    }
  }
])
