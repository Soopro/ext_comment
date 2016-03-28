angular.module('comment')

.service('extManager', function(){
  var last_body_height, interval;
  var html = document.documentElement;
  
  function postFrameHeight () {
    var html_height = Math.max(html.clientHeight,
                               html.scrollHeight,
                               html.offsetHeight);

    if (last_body_height != html_height){
      window.parent.postMessage({
        'height': html_height
      }, '*');
      last_body_height = html_height;
    }
  };
  
  if(window.parent && window.parent.postMessage){
    interval = setInterval(function() {
      postFrameHeight();
    }, 50);
  }
  
  function _clear () {
    if (interval) {
      clearInterval(interval);
    }
  };
  
  function _close () {
    _clear();
    window.parent.postMessage({
      'close': true
    }, '*');
  };
  function _flash (msg, is_error) {
    if(typeof angular.translate == 'function'){
      msg = angular.translate(msg)
    }
    window.parent.postMessage({
      'flash': {
        'msg': msg,
        'is_error': is_error
      }
    }, '*');
  };

  return {
    clear: _clear,
    close: _close,
    flash: _flash
  }
})