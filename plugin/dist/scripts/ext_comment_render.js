// Generated by CoffeeScript 1.10.0
(function() {
  var CASE_SENSITIVE, Comment, _, _all_basestring, _eventListeners, _trans_key, addListener, default_avatar, escape_html, get_comment_element, get_comment_key, get_comment_list, initHandler, last_value, load_dict, locale, locale_meta, localizedDict, localizedText, removeAllListeners, removeHandler, removeListeners, render_entry, render_outer, setLocale, submitHandler, translate, userLang;

  if (typeof document.querySelector !== 'function' || typeof document.addEventListener !== 'function') {
    console.log('SupExtComment: Your browser too old for this plugin.');
    return;
  }

  if (typeof SupExtComment !== 'function') {
    console.error('SupExtComment: not fully loaded!!');
    return;
  }

  default_avatar = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAHgAAAB4CAIAAAC2BqGFAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyhpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuNi1jMTExIDc5LjE1ODMyNSwgMjAxNS8wOS8xMC0wMToxMDoyMCAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENDIDIwMTUgKE1hY2ludG9zaCkiIHhtcE1NOkluc3RhbmNlSUQ9InhtcC5paWQ6MUU2NDczNjVGQjYwMTFFNUE2MkFDOUM5MDlDM0RFNjIiIHhtcE1NOkRvY3VtZW50SUQ9InhtcC5kaWQ6MUU2NDczNjZGQjYwMTFFNUE2MkFDOUM5MDlDM0RFNjIiPiA8eG1wTU06RGVyaXZlZEZyb20gc3RSZWY6aW5zdGFuY2VJRD0ieG1wLmlpZDoxRTY0NzM2M0ZCNjAxMUU1QTYyQUM5QzkwOUMzREU2MiIgc3RSZWY6ZG9jdW1lbnRJRD0ieG1wLmRpZDoxRTY0NzM2NEZCNjAxMUU1QTYyQUM5QzkwOUMzREU2MiIvPiA8L3JkZjpEZXNjcmlwdGlvbj4gPC9yZGY6UkRGPiA8L3g6eG1wbWV0YT4gPD94cGFja2V0IGVuZD0iciI/Pr8HBSkAAAO6SURBVHja7Nw/kyFBGAbwWZnMiphsiPyJTkYoZBN8BB/LR0CihEIyFykiJjMiNlOye27UbV3Z3cJ0T3fv9POEV3vdNT+v1jPT3S+Xy8Vh4s8LoQlNaIbQhCY0oQlNaIbQhCY0oQlNaIbQhCY0FQhNaIbQhI6YIAjW6/XhcDgej/v9/uPfXdfNZrO5XK5cLufzeUJHzOl0WiwWIIbv3T+GOLjr9frr6yuhH835fJ5Op8vlMsL/rdVqrVYrnU4T+k7gC2VYR24Byr1eDwVO6G8zHA6jFfKXpQ1uQn8xXIzH49VqJbHNarXa6XQMGUZShnzg0pURNIhmDbnAlCEjhnTlD2s0Tui/wQRO1rj83a8rurAdGkOzgopDFyLTmCRAC87knpqY2wuNe79YB42bAQTdWQo9n88T3J1B0JvNJsHdmQIdBMEjT4skBt2hU+ugtUy5fN+3saLVd7rb7ayD1jIH0Djx0Ab9/7uSZHdqyi24JSE0oQktJa7rWtKpZmgtr6s1viPXBq1lJUahULAOWstbas/zbKxoxV9kdKdxQZPOWYfiota70kMndKPRSHB3BkHju1yr1dT0hY70LsvTfMOiZp0cukBHVt8ZXtfJxd0LutC+Xkn/LTh+o2IdQDA0m7Dg0YhnHai4SqUSR8tott1um3CNpjxU6na70q3RIJo15AITu2wXI4YhtWwitBO+tBVcwcWF6I9GZGsFCrnZbHJrxRM5nU7z+RwF/sgbVdyMoIShzM1C0RMEge/7u90O4jfb38BaKBQ8z+P2N4bQhCY0Q2hCM4QmNKEZQhM6UnC3/f7+fl2gfzgcrg/zttvtzZ8Vi0UnfFyXy+WccCFSJpMx83GHKdBBGMjC9zPos8EHAHG458PYDo2y3Ww2vu9DNr79s6h3uHueVyqVNBa7BmjIrsMo3v7m/Dt6CVG/CE8d9FOHUSkQ/xVGWY2rgP4dRnzkjSMYVa7iPxsavrPZzIQSvlvgzWYzVu64oH8KsTJu+dAYi0ejkZkDxYODSbfblT52S4bGz91kMknAjdzb21u9XjcROo7z1PRG7mlucqChPBgMNG4Ajimu6/b7fSnWEqCTqizXWsIix+l0mlRlJ9ynL+XgK1HouE+tMyFSTs5LiZezY0HELzMl+FH/rFuSyMFlCn5xhaA1HlGkPoIXS+hHI3gIVErwC2UPtODMigejKAqhCU1ohtCEJjQJCE1ohtDGhst2CU1ohtCEJjShCU1ohtCEJjShCU1ohtCEJjShCU1ohtCEtjt/BBgAzHR+yWVd5VQAAAAASUVORK5CYII=';

  Comment = null;

  get_comment_element = function() {
    var el;
    el = document.querySelector('#sup-ext-comment-plugin');
    if (!el) {
      console.error('SupExtComment: no commment base element.');
    }
    return el;
  };

  get_comment_list = function() {
    var comm_element, comm_list;
    comm_element = get_comment_element();
    comm_list = comm_element.querySelector('.comm-list');
    if (!comm_list) {
      console.error('SupExtComment: no comment list.');
    }
    return comm_list;
  };

  get_comment_key = function() {
    var el, group_key, loc_group_key;
    el = get_comment_element();
    loc_group_key = window.location.hostname + location.pathname;
    group_key = el.getAttribute('group-key') || loc_group_key;
    return group_key;
  };

  escape_html = function(str) {
    var replace_tag, tagsToReplace;
    if (typeof str !== 'string') {
      return '';
    }
    tagsToReplace = {
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;'
    };
    replace_tag = function(tag) {
      return tagsToReplace[tag] || tag;
    };
    return str.replace(/[&<>]/g, replace_tag);
  };

  render_entry = function(entry) {
    var author_avatar, author_name, comm_list, entry_div, entry_inner, output_entry_author, remove_btn;
    comm_list = get_comment_list();
    if (!comm_list) {
      return;
    }
    if (entry.meta && entry.meta.author_name) {
      author_avatar = entry.meta.author_avatar || default_avatar;
      author_name = entry.meta.author_name;
      output_entry_author = '<img src="' + author_avatar + '" alt="' + author_name + '"/> <h5>' + author_name + '</h5>';
    } else {
      output_entry_author = '<h5>' + _('Anonymous') + '</h5>';
    }
    if (entry.is_author) {
      remove_btn = '<a href="#rm" class="remove-comment">' + _('Remove') + '</a>';
    } else {
      remove_btn = '';
    }
    entry_inner = '<div class="author-container">' + output_entry_author + '</div> <div class="comm-container"> <p>' + entry.content + '</p>' + remove_btn + '</div>';
    entry_div = document.createElement('div');
    entry_div.innerHTML = entry_inner;
    if (entry.is_author) {
      entry_div.dataset['entryId'] = entry.id;
    }
    entry_div.className = 'comm-entry';
    comm_list.appendChild(entry_div);
    return entry_div;
  };

  render_outer = function(author) {
    var comm_div, comm_element, output_author, output_outer;
    if (author) {
      output_author = '<img src="' + (author.avatar || default_avatar) + '" alt="' + author.name + '"/> <h5>' + author.name + '</h5>';
    } else {
      output_author = '<h5>' + _('Anonymous') + '</h5>';
    }
    output_outer = '<header> <h3>' + _('Comments') + '</h3> </header> <form name="sup-exts-comment-form" class="comm-form"> <div class="author-container">' + output_author + '</div> <div class="input-container"> <div> <textarea class="comm-textarea" placeholder="' + _('Your Comment here...') + '" rows="6"></textarea> </div> <button class="submit-comment btn btn-default" type="submit">' + _('Write your Comment') + '</button> </div> </form> <hr> <div class="comm-list"></div>';
    comm_div = document.createElement('div');
    comm_div.innerHTML = output_outer;
    comm_element = get_comment_element();
    comm_element.appendChild(comm_div);
    return comm_div;
  };

  _eventListeners = [];

  addListener = function(node, event, handler, capture) {
    _eventListeners.push({
      node: node,
      event: event,
      hanlder: handler,
      capture: capture
    });
    node.addEventListener(event, handler, capture);
  };

  removeListeners = function(node, event) {
    var i, idx, len, listener, remove_idxs;
    remove_idxs = [];
    for (idx = i = 0, len = _eventListeners.length; i < len; idx = ++i) {
      listener = _eventListeners[idx];
      if (event === listener.event && node === listener.node) {
        node.removeEventListener(event, listener.handler);
        remove_idxs.push(idx);
      }
    }
    _eventListeners.splice(remove_idxs, 1);
  };

  removeAllListeners = function() {
    var i, idx, len, listener;
    for (idx = i = 0, len = _eventListeners.length; i < len; idx = ++i) {
      listener = _eventListeners[idx];
      listener.node.removeEventListener(listener.event, listener.handler);
    }
    _eventListeners.length = 0;
  };

  last_value = null;

  submitHandler = function(e) {
    var btn, data, error1, params, ta, value;
    e.preventDefault();
    btn = e.target;
    ta = btn.parentElement.querySelector('.comm-textarea');
    try {
      value = ta.value.trim();
    } catch (error1) {
      value = null;
    }
    value = escape_html(value);
    if (last_value === value) {
      return;
    } else {
      last_value = value;
    }
    if (value && typeof value === 'string') {
      params = {
        key: get_comment_key()
      };
      data = {
        content: value
      };
      btn.disabled = true;
      Comment.add(params, data).then(function(data) {
        var el, new_btn;
        el = render_entry(data);
        new_btn = el.querySelector('.remove-comment');
        return addListener(new_btn, 'click', removeHandler);
      })["catch"](function(error) {
        return console.error(error);
      })["finally"](function() {
        return btn.disabled = false;
      });
    }
    return false;
  };

  removeHandler = function(e) {
    var btn, entry, params, parent;
    e.preventDefault();
    btn = e.target;
    if (btn.hasAttribute('disabled')) {
      return false;
    }
    parent = btn.parentElement;
    entry = null;
    while (true) {
      if (parent.className.indexOf('comm-entry') > -1) {
        entry = parent;
        break;
      }
      parent = parent.parentElement;
    }
    if (!entry) {
      console.error('SupExtComment: entry not found.');
      return;
    }
    params = {
      key: get_comment_key(),
      id: entry.dataset['entryId']
    };
    btn.setAttribute('disabled', true);
    Comment.remove(params).then(function(data) {
      removeListeners(btn, 'click');
      return entry.parentElement.removeChild(entry);
    })["catch"](function(error) {
      return console.error(error);
    })["finally"](function() {
      return btn.removeAttribute('disabled');
    });
    return false;
  };

  initHandler = function() {
    var api_url, app_open_id, comm_element, opts;
    setLocale(locale);
    comm_element = get_comment_element();
    if (!comm_element) {
      return;
    }
    api_url = comm_element.getAttribute('api-url');
    app_open_id = comm_element.getAttribute('app-open-id');
    opts = {};
    if (api_url) {
      opts.apiExtURL = api_url;
    }
    if (app_open_id) {
      opts.app_id = app_open_id;
    }
    Comment = new SupExtComment(opts);
    Comment.query({
      key: get_comment_key()
    }).then(function(comments) {
      var author, btn, entry, form, i, j, len, len1, remove_btns, results;
      author = Comment.author.profile();
      render_outer(author);
      for (i = 0, len = comments.length; i < len; i++) {
        entry = comments[i];
        render_entry(entry);
      }
      form = comm_element.querySelector('.comm-form .submit-comment');
      addListener(form, 'click', submitHandler);
      remove_btns = comm_element.querySelectorAll('.remove-comment');
      results = [];
      for (j = 0, len1 = remove_btns.length; j < len1; j++) {
        btn = remove_btns[j];
        results.push(addListener(btn, 'click', removeHandler));
      }
      return results;
    })["catch"](function(error) {
      return console.error(error);
    });
  };

  document.addEventListener('DOMContentLoaded', initHandler);

  locale = null;

  locale_meta = document.querySelector('meta[name="locale"]');

  if (locale_meta) {
    locale = locale_meta.getAttribute('content');
  }

  if (!locale) {
    userLang = navigator.language || navigator.userLanguage;
    locale = userLang.replace('-', '_');
  }

  if (!locale) {
    locale = 'en_US';
  }

  localizedText = {};

  localizedDict = {};

  CASE_SENSITIVE = false;

  _all_basestring = function() {
    var arg, i, len;
    for (i = 0, len = arguments.length; i < len; i++) {
      arg = arguments[i];
      if (typeof arg !== 'string') {
        return false;
      }
    }
    return true;
  };

  _trans_key = function(str) {
    if (!CASE_SENSITIVE) {
      return str.toLowerCase();
    }
    return str;
  };

  load_dict = function(loc_texts) {
    var i, len, loc_text_dict, text;
    loc_text_dict = {};
    if (Object.prototype.toString.call(loc_texts) === '[object Array]') {
      for (i = 0, len = loc_texts.length; i < len; i++) {
        text = loc_texts[i];
        if (_all_basestring(text.msgid, text.msgid) && text.msgid) {
          loc_text_dict[_trans_key(text.msgid)] = text.msgstr;
        }
      }
    } else if (loc_texts && typeof loc_texts === 'object') {
      loc_text_dict = loc_texts;
    }
    return loc_text_dict;
  };

  setLocale = function(loc) {
    var k, locale_dict, v;
    if (!loc) {
      loc = '';
    }
    locale = null;
    loc = loc.replace('-', '_');
    for (k in localizedDict) {
      v = localizedDict[k];
      if (k.toLowerCase() === loc.toLowerCase()) {
        locale = k;
        break;
      }
    }
    if (locale && localizedDict[locale]) {
      locale_dict = localizedDict[locale];
    } else {
      locale_dict = null;
      locale = loc;
    }
    localizedText = load_dict(locale_dict);
    return locale;
  };

  translate = function(text) {
    var arg, args, i, j, len, len1, ref, trans;
    if (!text || typeof text !== 'string') {
      return text;
    }
    trans = localizedText[_trans_key(text)];
    if (!trans) {
      trans = text;
    }
    args = [];
    for (i = 0, len = arguments.length; i < len; i++) {
      arg = arguments[i];
      args.push(arg);
    }
    ref = args.slice(1);
    for (j = 0, len1 = ref.length; j < len1; j++) {
      arg = ref[j];
      if (arg === void 0) {
        arg = '';
      }
      trans = trans.replace("%s", arg);
    }
    return trans;
  };

  _ = translate;

  localizedDict['zh_CN'] = [
    {
      'msgid': 'Comments',
      'msgstr': '评论'
    }, {
      'msgid': 'Your Comment here...',
      'msgstr': '在这里写上您的评论...'
    }, {
      'msgid': 'Anonymous',
      'msgstr': '匿名'
    }, {
      'msgid': 'Remove',
      'msgstr': '移除'
    }, {
      'msgid': 'Write your Comment',
      'msgstr': '写下您的评论'
    }
  ];

}).call(this);
