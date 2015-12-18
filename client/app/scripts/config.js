'use strict';

angular.module('commentClient')
.constant('Config', {
  api: "http://127.0.0.1:5001/comment",
  auth_api: "http://127.0.0.1:5001/comment/user",
});
