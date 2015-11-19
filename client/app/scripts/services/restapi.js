'use strict';

/**
 * @ngdoc service
 * @name commentClient.restapi
 * @description
 * # restapi
 * Factory in the commentClient.
 */
angular.module('commentClient')
.factory('restAPI', function ($resource, Config) {
  // Service logic
  // ...
  var api = Config.api;
  var auth_api = Config.auth_api;

  // Public API here
  return {
    comment: (function () {
      return $resource(api+"/visit/group/:group_key");
    })(),
    remove_comment: (function () {
      return $resource(api+"/visit/group/:group_key/:comment_id");
    })(),


    comment_extension: (function () {
      return $resource(api+"/manage/settings/:open_id");
    })(),

    list_comment_groups: (function () {
      return $resource(api+"/manage/group");
    })(),

    group_comments: (function () {
      return $resource(api+"/manage/group/:group_key");
    })(),


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
});
