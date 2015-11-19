/**
 * @ngdoc function
 * @name commentClient.controller:CommentsCtrl
 * @description
 * # CommentsCtrl
 * Controller of the commentClient
 */

angular.module('commentClient')
.controller('CommentsCtrl', function($scope, $location) {
  'use strict';
  $scope.comments = [{
    content: 'GSecondary line text Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam massa quam. Nulla metus metus, ullamcorper vel, tincidunt sed, euismod in, nibh. Quisque volutpat condimentum velit. Class aptent taciti sociosqu ad litra torquent per conubia nostra, per inceptos himenaeos.',
    author_name: 'Min Li Chan',
    creation: 'Using the aria-label attribute - Accessibility | MDN'
  }, {
    content: 'Gasdfasdfasdfasdfj',
    author_name: 'Min Li Chan',
    creation: 'Using the aria-label attribute - Accessibility | MDN'
  }, {
    content: 'Gasdfasdfasdfasdf',
    author_name: 'Min Li Chanyj',
    creation: 'Using the aria-label attribute - Accessibility | MDN'
  }, {
    content: 'Gasdfasdfasdfasdf',
    author_name: 'Min Li Chantg',
    creation: 'Using the aria-label attribute - Accessibility | MDN'
  }, {
    content: 'Gasdfasdfasdfasdf',
    author_name: 'Min Li Chands',
    creation: 'Using the aria-label attribute - Accessibility | MDN'
  }];

  $scope.jumpToIndex = function() {
    $location.path('/');
  };
});
