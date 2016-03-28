angular.module('comment')

.factory('restUser', [
  'supResource',
  'Config',

  function (
    supResource,
    Config
  ){
    'use strict';

    var api = Config.baseURL.api+'/user';

    var res = {
      auth: supResource(api+'/:open_id', {
        open_id: '@open_id'
      }, {
        'access': {method: 'POST'},
        'logout': {method: 'DELETE'}
      }),
      checker: supResource(api+'/:open_id/check', {
        open_id: '@open_id'
      }, {
        'check': {method: 'POST'},
      })
    };

    return res;
  }
])
