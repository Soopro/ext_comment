'use strict';

angular.module('commentClient')
.constant('Config', function(){
  var test = {
    api: "http://127.0.0.1:5001/comment",
    auth_api: "http://127.0.0.1:5001/comment/user",
  }
  
  var dev = {
    api: "http://127.0.0.1:5001/comment",
    auth_api: "http://127.0.0.1:5001/comment/user",
  }
  
  var prd = {
    api: "http://ext.soopro.com/comment/server/comment",
    auth_api: "http://ext.soopro.com/comment/server/comment/user",
  }
  
  var config = dev
  
  return config
  
}());
