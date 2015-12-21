'use strict';

angular.module('commentClient')
.factory(
  'interceptor', 
  function (
    $q,
    $location,
    Auth,
    Config
  ) {
  // Service logic
  // Public API here
  return {
    request: function (request) {
      request.headers = request.headers || {};
      if (Auth.getToken()) {
        request.headers.Authorization = Auth.getToken();
      }
      console.log('request')
      console.log(request)
      return request;
    },
    response: function (response) {
      console.log('response')
      console.log(response)
      return response ? response : $q.when(response);
    },
      //     responseError: function (rejection) {
      //       if (rejection.status==0 && rejection.data == null){
      //         $location.path('/404');
      //       }
      //       if (rejection.status==401) {
      //         $location.path('/auth');
      //       }
      // try {
      //   console.error({
      //     errmsg: rejection.data.errmsg,
      //     erraffix: rejection.data.erraffix,
      //     errcode: rejection.data.errcode,
      //     rejection: rejection
      //   });
      //       }catch(e){
      //         console.error(rejection, e);
      //       }
      //       return $q.reject(rejection);
      //     }
  };
})
.config(function($httpProvider) {
  $httpProvider.interceptors.push('interceptor');
});