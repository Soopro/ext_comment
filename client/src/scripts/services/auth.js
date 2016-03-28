angular.module('comment')

.service('Auth', [
  '$cookies',
  'Config',
  
  function(
    $cookies,
    Config
  ){
    'use strict';
    var storage = window.localStorage;

    var ext_token = storage.getItem('token') ? storage.getItem('token') : null;

    var hanlder = {
      is_logged: function() {
        return ext_token ? true : false;
      },
      set_token: function(token) {
        storage.setItem('token', token)
      },
      get_token: function() {
        return storage.getItem('token')
      },
      set_open_id: function(open_id) {
        storage.setItem('open_id', open_id);
      },
      get_open_id: function() {
        return storage.getItem('open_id');
      },
      set_oauth_page: function(oauth_page_uri) {
        storage.setItem('oauth_page_uri', oauth_page_uri)
      },
      get_oauth_page: function() {
        return storage.getItem('oauth_page_uri')
      },
      logout: function() {
        storage.removeItem('token')
      },
      clean: function() {
        storage.clear()
      }
    }
    return hanlder;

    // var ext_token = $cookies.get('token') ? $cookies.get('token') : null;
    //
    // var hanlder = {
    //   is_logged: function() {
    //     return ext_token? true : false;
    //   },
    //   set_token: function(token) {
    //     $cookies.put('token', token)
    //   },
    //   get_token: function() {
    //     return $cookies.get('token')
    //   },
    //   set_open_id: function(open_id) {
    //     $cookies.put('open_id', open_id);
    //   },
    //   get_open_id: function() {
    //     return $cookies.get('open_id')
    //   },
    //   set_oauth_page: function(oauth_page_uri) {
    //     $cookies.put('oauth_page_uri', oauth_page_uri)
    //   },
    //   get_oauth_page: function() {
    //     return $cookies.get('oauth_page_uri')
    //   },
    //   logout: function() {
    //     $cookies.remove('token')
    //   },
    //   clean: function() {
    //     $cookies.remove('token')
    //         $cookies.remove('open_id')
    //     $cookies.remove('oauth_page_uri')
    //   }
    // }
    // return hanlder;
  }
])
