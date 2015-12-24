'use strict';

angular.module('commentClient')
.factory('restAPI', [
  '$resource',
  'Config',
  function (
    $resource, 
    Config
  ) {
  // Service logic
  // ...
  var api = Config.api;
  var auth_api = Config.auth_api;

  return {
    
    // apis for visitors
    visit_group: (function () {
      return $resource(api+"/visit/group/:group_key");
    })(),
    visit_comment: (function () {
      return $resource(api+"/visit/group/:group_key/comment/:comment_id");
    })(),
    
    // apis for admins
    admin_extension: (function () {
      return $resource(api+"/admin/extension/:extension_id");
    })(),

    // admin_groups: (function () {
    //   return $resource(api+"/admin/group");
    // })(),

    admin_group: (function () {
      return $resource(api+"/admin/group/:group_id");
    })(),
    
    admin_comment: (function () {
      return $resource(api+"/admin/group/:group_id/comment");
    })(),
    
    // admin_remove_comment: (function () {
    //   return $resource(api+"/admin/group/:group_key/:comment_id");
    // })(),

    // apis for auth
    alias: (function () {
      return $resource(auth_api+"/alias");
    })(),
    ext_token: (function () {
      return $resource(auth_api+"/ext_token/:open_id");
    })(),
    sup_auth: (function () {
      return $resource(auth_api+"/sup_auth");
    })(),
    token_check: (function () {
      return $resource(auth_api+"/token_check");
    })()
  };
}]);
