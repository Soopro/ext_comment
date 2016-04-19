/* -------------------------------
 * Server Conf: sup ext comment
/* ------------------------------- */

if (sup_ext_comment == 'undefined' || !sup_ext_comment){
   var sup_ext_comment = {}
}

var test = {
  'api': 'http://ext.sup.farm/comment/server'
}

var dev = {
  'api': 'http://localhost:5001'
}

var prd = {
  'api': 'http://api-comm.exts.soopro.net'
}

sup_ext_comment.server = dev;
sup_ext_comment.is_debug = true;
