'use strict';

/**
 * @ngdoc function
 * @name commentClient.controller:AuthCtrl
 * @description
 * # AuthCtrl
 * Controller of the url4Client
 */
angular.module('commentClient')
.controller('AuthCtrl', function ($window, $routeParams, Auth, restAPI, Config, $location) {

  // get remote redirect info from ext server.
  var goPlatfromLogin = function () {
    if ($routeParams.open_id) {
      var open_id = $routeParams.open_id;
      Auth.cleanAuth();
      Auth.setOpenId(open_id);
      console.log(Auth.getOpenId())

      restAPI.ext_token.get({open_id: open_id})
      .$promise
      .then(function (data) {
        if (data.state) {
          var redirect_uri = encodeURIComponent(data.redirect_uri)
            
          $window.location = data.auth_uri +
          '?open_id=' + open_id +
          '&state=' + data.state +
          '&app_key=' + data.app_key +
          '&response_type=' + data.response_type +
          '&redirect_uri=' + redirect_uri;
        }
      })
			.catch(function (data) {
				console.error(data)
			})
    }
    else {
      alert('open_id is required!')
    }
  };
  
  // get current token from cookie
  var extToken = Auth.getToken();
  
  if (!extToken) {
    // get new  token from remote if no token in cookies.
    getToken()
  } else {
    restAPI.token_check.save({},{ext_token: extToken})
    .$promise
    .then(function (data){
      $location.url('/')
    })
    .catch(function(error){
      getToken()
    })
  }
});
