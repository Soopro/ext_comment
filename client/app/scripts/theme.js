'use strict';

angular.module('commentClient')
.config([
  '$mdIconProvider', 
  function($mdIconProvider) {
    return $mdIconProvider
      .iconSet('alert', '/styles/icons/svg-sprite-alert.svg', 24)
  }
]);