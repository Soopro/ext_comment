angular.module('comment')

.service('fsv', function() {
  function fsv (form, args) {
    if (!form) {
      console.error(form, "Form is not exist");
      return false;
    }
    if (!form.$valid) {
      for (i = 0; i < args.length; i++) {
        var arg = args[i];
        if (form[arg]) {
          form[arg].$touched = true;
          form[arg].$dirty = true;
        } else {
          console.warn(
            "Form Submit Validation Error: "+"'"+arg+"' is undefined");
        }
      }
      return false;
    } else {
      return true;
    }
  };
  return fsv
})
