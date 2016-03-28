angular.module('comment')

.controller('authCtrl', [
  '$scope',
  '$window',
  '$location',
  '$routeParams',
  'Auth',
  'restUser',
  'Config',

  function(
    $scope,
    $window,
    $location,
    $routeParams,
    Auth,
    restUser,
    Config
  ){
    'use strict';

    var open_id = $routeParams.open_id || Auth.get_open_id();
    var oauth_page_uri = $routeParams.oauth_page_uri || Auth.get_oauth_page();
    
    if (!open_id || typeof(open_id) != 'string'){
      console.error('Open id is required!')
      $location.path(Config.route.error)
      return;
    }

    // get remote redirect info from ext server.
    function get_token (open_id) {
      if (open_id) {
        
        Auth.set_open_id(open_id);
        Auth.set_oauth_page(oauth_page_uri);

        var auth = new restUser.auth({
          open_id: open_id
        })
        
        auth.$get()
        .then(function (data) {
          if (data.state) {
            var pair;
            if (oauth_page_uri.indexOf('?') < 0){
              pair = '?';
            } else {
              pair = '&';
            }
            $window.location = oauth_page_uri + pair +
            'open_id=' + open_id +
            '&state=' + data.state +
            '&ext_key=' + data.ext_key +
            '&response_type=' + data.response_type +
            '&redirect_uri=' + encodeURIComponent(data.redirect_uri);
          }
        })
				.catch(function (data) {
					console.error(data)
          $location.path(Config.route.error)
				})
      }
    };
    
    // get current token from cookie
    var ext_token = Auth.get_token();
    if (!ext_token) {
      get_token(open_id)
    } else {
      var token = new restUser.checker({
        open_id: open_id
      })
      token.$check()
      .then(function (data){
        if (data.result) {
          $location.path(Config.route.portal)
        } else {
          get_token(open_id)
        }
      })
    }
  }
])
