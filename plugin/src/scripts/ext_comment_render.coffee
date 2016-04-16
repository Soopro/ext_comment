# -------------------------------
# Comment Extension Render.
# -------------------------------

if typeof document.querySelector isnt 'function' \
or typeof document.addEventListener isnt 'function'
  console.log 'SupExtComment: Your browser too old for this plugin.'
  return

if typeof SupExtComment isnt 'function'
  console.error 'SupExtComment not fully loaded!!'
  return

# globals

default_avatar = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAHgAAAB4CAIAAAC2BqGFAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyhpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuNi1jMTExIDc5LjE1ODMyNSwgMjAxNS8wOS8xMC0wMToxMDoyMCAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENDIDIwMTUgKE1hY2ludG9zaCkiIHhtcE1NOkluc3RhbmNlSUQ9InhtcC5paWQ6MUU2NDczNjVGQjYwMTFFNUE2MkFDOUM5MDlDM0RFNjIiIHhtcE1NOkRvY3VtZW50SUQ9InhtcC5kaWQ6MUU2NDczNjZGQjYwMTFFNUE2MkFDOUM5MDlDM0RFNjIiPiA8eG1wTU06RGVyaXZlZEZyb20gc3RSZWY6aW5zdGFuY2VJRD0ieG1wLmlpZDoxRTY0NzM2M0ZCNjAxMUU1QTYyQUM5QzkwOUMzREU2MiIgc3RSZWY6ZG9jdW1lbnRJRD0ieG1wLmRpZDoxRTY0NzM2NEZCNjAxMUU1QTYyQUM5QzkwOUMzREU2MiIvPiA8L3JkZjpEZXNjcmlwdGlvbj4gPC9yZGY6UkRGPiA8L3g6eG1wbWV0YT4gPD94cGFja2V0IGVuZD0iciI/Pr8HBSkAAAO6SURBVHja7Nw/kyFBGAbwWZnMiphsiPyJTkYoZBN8BB/LR0CihEIyFykiJjMiNlOye27UbV3Z3cJ0T3fv9POEV3vdNT+v1jPT3S+Xy8Vh4s8LoQlNaIbQhCY0oQlNaIbQhCY0oQlNaIbQhCY0FQhNaIbQhI6YIAjW6/XhcDgej/v9/uPfXdfNZrO5XK5cLufzeUJHzOl0WiwWIIbv3T+GOLjr9frr6yuhH835fJ5Op8vlMsL/rdVqrVYrnU4T+k7gC2VYR24Byr1eDwVO6G8zHA6jFfKXpQ1uQn8xXIzH49VqJbHNarXa6XQMGUZShnzg0pURNIhmDbnAlCEjhnTlD2s0Tui/wQRO1rj83a8rurAdGkOzgopDFyLTmCRAC87knpqY2wuNe79YB42bAQTdWQo9n88T3J1B0JvNJsHdmQIdBMEjT4skBt2hU+ugtUy5fN+3saLVd7rb7ayD1jIH0Djx0Ab9/7uSZHdqyi24JSE0oQktJa7rWtKpZmgtr6s1viPXBq1lJUahULAOWstbas/zbKxoxV9kdKdxQZPOWYfiota70kMndKPRSHB3BkHju1yr1dT0hY70LsvTfMOiZp0cukBHVt8ZXtfJxd0LutC+Xkn/LTh+o2IdQDA0m7Dg0YhnHai4SqUSR8tott1um3CNpjxU6na70q3RIJo15AITu2wXI4YhtWwitBO+tBVcwcWF6I9GZGsFCrnZbHJrxRM5nU7z+RwF/sgbVdyMoIShzM1C0RMEge/7u90O4jfb38BaKBQ8z+P2N4bQhCY0Q2hCM4QmNKEZQhM6UnC3/f7+fl2gfzgcrg/zttvtzZ8Vi0UnfFyXy+WccCFSJpMx83GHKdBBGMjC9zPos8EHAHG458PYDo2y3Ww2vu9DNr79s6h3uHueVyqVNBa7BmjIrsMo3v7m/Dt6CVG/CE8d9FOHUSkQ/xVGWY2rgP4dRnzkjSMYVa7iPxsavrPZzIQSvlvgzWYzVu64oH8KsTJu+dAYi0ejkZkDxYODSbfblT52S4bGz91kMknAjdzb21u9XjcROo7z1PRG7mlucqChPBgMNG4Ajimu6/b7fSnWEqCTqizXWsIix+l0mlRlJ9ynL+XgK1HouE+tMyFSTs5LiZezY0HELzMl+FH/rFuSyMFlCn5xhaA1HlGkPoIXS+hHI3gIVErwC2UPtODMigejKAqhCU1ohtCEJjQJCE1ohtDGhst2CU1ohtCEJjShCU1ohtCEJjShCU1ohtCEJjShCU1ohtCEtjt/BBgAzHR+yWVd5VQAAAAASUVORK5CYII='


Comment = null

get_comment_element = ->
  el = document.querySelector('#sup-comment-exts-plugin')
  return el

get_comment_key = ->
  el = get_comment_element()
  group_key = el.getAttribute('group-key') or location.href
  return group_key

escape_html = (str)->
  tagsToReplace =
    '&': '&amp;'
    '<': '&lt;'
    '>': '&gt;'

  replace_tag = (tag)->
    return tagsToReplace[tag] or tag

  return str.replace(/[&<>]/g, replace_tag)


# renders
render_entry = (entry)->
  if entry.meta and entry.meta.author_name
    author_avatar = entry.meta.author_avatar or default_avatar
    author_name = entry.meta.author_name
    output_entry_author = '
      <img src="'+author_avatar+'" alt="'+author_name+'"/>
      <h5>'+author_name+'</h5>
    '
  else
    output_entry_author = '<h5>'+_('Anonymous')+'</h5>'

  if entry.author
    remove_btn = '<a href="#" class="remove-comment">'+_('Remove')+'</a>'
    output_entry_id = 'data-entry-id="'+entry.id+'"'
  else
    remove_btn = ''
    output_entry_id = ''

  output_entry = '
    <div class="comm-entry" '+output_entry_id+'>
      <div class="author-container">
        '+output_entry_author+'
      </div>
      <div class="comm-container">
        <p>'+entry.content+'</p>
        '+remove_btn+'
      </div>
    </div>
  '
  return output_entry


render_list = (author, comm_items)->
  if author
    output_author = '
      <img src="'+(author.avatar or default_avatar)+'"
       alt="'+author.name+'"/>
      <h5>'+author.name+'</h5>
    '
  else
    output_author = '<h5>'+_('Anonymous')+'</h5>'

  output_comm_items = ''
  for item in comm_items
    output_comm_items += render_entry(item)


  output = '
  <header>
    <h3>'+_('Comments')+'</h3>
  </header>
  <form name="sup-exts-comment-form" class="comm-form">
    <div class="author-container">
      '+output_author+'
    </div>
    <div class="input-container">
      <div>
        <textarea class="comm-textarea"
                  placeholder="'+_('Your Comment here...')+'"
                  rows="6"></textarea>
      </div>
      <button class="submit-comment btn btn-default" type="submit">
        '+_('Write your Comment')+'
      </button>
    </div>
  </form>
  <hr>
  <div class="comm-list">
    '+output_comm_items+'
  </div>
  '


# lisenters
_eventListeners = []

addListener = (node, event, handler, capture)->
  _eventListeners.push {
    node: node
    event: event
    hanlder: handler
    capture: capture
  }
  node.addEventListener event, handler, capture
  return

removeListeners = (node, event) ->
  remove_idxs = []
  for listener, idx in _eventListeners
    if event == listener.event and node == listener.node
      node.removeEventListener event, listener.handler
      remove_idxs.push idx
  _eventListeners.splice(remove_idxs, 1)
  return

removeAllListeners = ->
  for listener, idx in _eventListeners
    listener.node.removeEventListener listener.event, listener.handler
  _eventListeners.length = 0
  return


submitHandler = (e)->
  e.preventDefault()
  ta = e.target.parentElement.querySelector('.comm-textarea')
  try
    value = ta.value.trim()
  catch
    value = null

  value = escape_html(value)

  if value and typeof value is 'string'
    params =
      key: get_comment_key()
    data =
      content: value
    Comment.add(params, data)
    .then (data)->
      console.log data
    .catch (error)->
      console.error error.data

  return false


removeHandler = (e)->
  console.log e
  e.preventDefault()
  return false


# init


initHandler = ->

  # init locale
  setLocale(locale)

  # init comment
  comm_element = get_comment_element()
  if not comm_element
    return

  api_url = comm_element.getAttribute('api-url')
  opts = {}
  if api_url
    opts.apiExtURL = api_url

  Comment = new SupExtComment(opts)

  # render elements
  Comment.query({key: get_comment_key()})

  .then (comments)->

    author = Comment.author.profile()
    comm_element.innerHTML = render_list(author, comments)

    form = comm_element.querySelector('.comm-form .submit-comment')
    addListener(form, 'click', submitHandler)

    remove_btns = comm_element.querySelectorAll('.remove-comment')
    for btn in remove_btns
      addListener(btn, 'click', removeHanlder)

  .catch (error)->
    console.log error.data

  return

document.addEventListener 'DOMContentLoaded', initHandler


# languages
locale = null

locale_meta = document.querySelector('meta[name="locale"]')
if locale_meta
  locale = locale_meta.getAttrbutie('content')

if not locale
  userLang = navigator.language or navigator.userLanguage
  locale = userLang.replace('-','_')

if not locale
  locale = 'en_US'

localizedText = {}
localizedDict = {}
CASE_SENSITIVE = false

_all_basestring = ->
  for arg in arguments
    if typeof(arg) != 'string'
      return false
  return true

_trans_key = (str)->
  if not CASE_SENSITIVE
    return str.toLowerCase()
  return str


load_dict = (loc_texts)->
  loc_text_dict = {}

  if Object.prototype.toString.call(loc_texts) == '[object Array]'
    for text in loc_texts
      if _all_basestring(text.msgid, text.msgid) and text.msgid
        loc_text_dict[_trans_key(text.msgid)] = text.msgstr
  else if loc_texts and typeof(loc_texts) == 'object'
    loc_text_dict = loc_texts

  return loc_text_dict


setLocale = (loc) ->
  if not loc
    loc = ''
  locale = null
  loc = loc.replace('-','_')

  for k,v of localizedDict
    if k.toLowerCase() is loc.toLowerCase()
      locale = k
      break

  if locale and localizedDict[locale]
    locale_dict = localizedDict[locale]
  else
    locale_dict = null
    locale = loc

  localizedText = load_dict(locale_dict)

  return locale


translate = (text) ->
  if not text or typeof text isnt 'string'
    return text

  trans = localizedText[_trans_key(text)]
  if not trans
    trans = text

  args=[]
  for arg in arguments
    args.push arg

  for arg in args[1..]
    arg = '' if arg is undefined
    trans = trans.replace("%s", arg)

  return trans

_ = translate

# language dict

localizedDict['zh_CN'] = [
  {
    'msgid': 'Comments'
    'msgstr': '评论'
  }
  {
    'msgid': 'Your Comment here...'
    'msgstr': '在这里写上您的评论...'
  }
  {
    'msgid': 'Anonymous'
    'msgstr': '匿名'
  }
  {
    'msgid': 'Remove'
    'msgstr': '移除'
  }
  {
    'msgid': 'Write your Comment'
    'msgstr': '写下您的评论'
  }
]