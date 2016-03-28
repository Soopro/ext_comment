'use strict';

angular.module('comment')
.filter("dateformat", [
  '$filter', 
  
  function(
    $filter
  ) {
    return function(date, format) {
      var count;
      if (!format) {
        format = 'medium';
      }
      if (typeof angular.translate === 'function') {
        format = angular.translate(format);
      }
      count = 0;
      if (typeof date === 'number') {
        count = date.toString().length;
      }
      if (count === 10) {
        date = date * 1000;
      }
      return $filter('date')(date, format);
    };
  }
]);

