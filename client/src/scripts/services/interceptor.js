angular.module('comment')

.factory('interceptor', [
  '$q',
  '$location',
  'Auth',
  'extManager',
  'Config',

  function(
    $q,
    $location,
    Auth,
    extManager,
    Config
  ){
    'use strict';
    
    var retry = 0;
    
    var interceptor = {
      request: function (request) {
        request.headers = request.headers || {};
        var token = Auth.get_token()
        if (token) {
          request.headers.Authorization = 'Bearer '+token
        }
        return request;
      },
      response: function (response) {
        retry = 0;
        return response ? response : $q.when(response)
      },
      responseError: function (rejection) {
        var reject_url = rejection.config.url;
        var is_api_reject = reject_url.indexOf(Config.baseURL.api) == 0;
        if (!is_api_reject){
          console.log ('Request is rejected by remote.')
        } else {
          if (rejection.status == 0 && rejection.data == null){
            $location.path(Config.route.error);
            console.error('Error! No connection to server.')
          }
          if (rejection.status == 401) {
            Auth.logout();
            if(retry < 3){
              retry += 1;
              $location.path(Config.route.auth);
            } else {
              $location.path(Config.route.error);
            }
          } else if (rejection.status == 404){
            $location.path(Config.route.error);
          }
          if (rejection.data && rejection.data.errmsg
                             && rejection.status != 200){
            console.error(rejection.data)
            extManager.flash(rejection.data.errmsg, true)
          }
        }
        return $q.reject(rejection);
      }
    };
    return interceptor
  }
])

.config([
  '$httpProvider',

  function(
    $httpProvider
  ){
    $httpProvider.interceptors.push('interceptor');
  }
])
