angular.module('comment')

.constant('Config', {
  'baseURL': {
    'api': sup_ext_comment.server.api
  },
  
  'debug': sup_ext_comment.is_debug,
  
  'route': {
    portal: '/comment',
    auth: '/auth',
    error: '/404',
  },

});
