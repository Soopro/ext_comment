'use strict';

angular.module('commentClient')
.service('flash', [
  '$interval', 
  '$mdToast',
  function(
    $interval, 
    $mdToast
  ) {
    return function(msg, warn, opts) {
      var flash, preset;
      if (!opts) {
        opts = {};
      }
      if (!opts.pos) {
        opts.pos = "top right";
      }
      if (!opts.delay) {
        opts.delay = 4000;
      }
      preset = {
        template: [
          '<md-toast md-theme="{{ opts.theme }}" class="text-nowrap"', 
           'ng-class="{\'md-capsule\': opts.capsule, ',
           '\'md-warn\': opts.warn}">', 
            '<span flex>', 
              '<md-icon ng-if="opts.warn" ', 
               'md-svg-icon="alert:ic_warning_24px"></md-icon> ', 
              '{{ content }}', 
            '</span>', 
            '<md-button class="md-action" ng-if="opts.action" ', 
             'ng-click="resolve()" ', 
             'ng-class="{\'md-highlight\': opts.highlight}">', 
              '{{ opts.action }}', 
            '</md-button>', 
          '</md-toast>'
        ].join(''),
        locals: {
          content: msg,
          opts: {
            warn: warn,
            action: opts.action,
            highlight: opts.highlight,
            capsule: opts.capsule
          }
        },
        controller: 'flashToastCtrl',
        position: opts.pos,
        hideDelay: opts.delay
      };
      flash = $mdToast.build(preset);
      return $mdToast.show(flash);
    };
  }
]).controller('flashToastCtrl', [
  '$scope', 
  '$mdToast', 
  'content', 
  'opts', 
  function(
    $scope, 
    $mdToast, 
    content, 
    opts
  ) {
    $scope.content = content;
    $scope.opts = opts;
    return $scope.resolve = function() {
      return $mdToast.hide();
    };
  }
]);

