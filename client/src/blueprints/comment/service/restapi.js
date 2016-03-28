angular.module('comment')

.factory('restAPI', [
  'supResource',
  'Config',

  function (
    supResource,
    Config
  ){
    'use strict';
  
    var api = Config.baseURL.api + '/comment';
    

    var res = {
      extension: supResource(api+"/admin/extension/:extension_id"),

      admin_group: supResource(api+"/admin/group/:group_id"),
    
      admin_comment: supResource(api+"/admin/group/:group_id/comment"),
      
      batch_comment: supResource(api+"/admin/group/:group_id/comment/batch", {
        group_id: '@group_id'
      }, {
        batch_delete: {method: 'POST'},
      }
                                  )
    };
  
    return res;
  }
])
