/** 
 * description
 * # interceptor
 * Factory in the commentClient.
 */
angular.module('commentClient')
.factory('interceptor', function ($q,$location,Auth,Config) {
  // Service logic
  // Public API here
  return {
    request: function (request) {
      request.headers = request.headers || {};
      if (Auth.getToken()) {
        request.headers.Authorization = Auth.getToken()
      }
      return request;
    },
    response: function (response) {
      return response ? response : $q.when(response)
    },
    responseError: function (rejection) {
      if (rejection.status===0 && rejection.data === null){
        $location.path('/404');
      }
      if (rejection.status===401) {
        $location.path('/auth');
      }
      return $q.reject(rejection);
    }
  };
})
.config(function($httpProvider) {
  $httpProvider.interceptors.push('interceptor');
});