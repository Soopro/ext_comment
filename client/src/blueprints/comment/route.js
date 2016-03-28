angular.module('comment')

.config([
  '$routeProvider',
  
  function(
    $routeProvider
  ){
    var bp = "comment";
    var dir = "blueprints/comment/views";

    $routeProvider
    
    .when('/' + bp + '/', {
      redirectTo: '/' + bp + '/groups'
    })
    
    .when('/' + bp + '/settings', {
      templateUrl: dir + "/settings.html",
      controller: "settingsCtrl"
    })
    
    .when('/' + bp + '/groups', {
      templateUrl: dir + "/groups.html",
      controller: "groupsCtrl"
    })
    
    .when('/' + bp + '/groups/:group_id', {
      templateUrl: dir + "/comments.html",
      controller: "commentsCtrl"
    });
  }
]);