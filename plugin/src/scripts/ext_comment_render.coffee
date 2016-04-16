# -------------------------------
# Comment Extension Render.
# -------------------------------

default_avatar = 'styles/default_avatar.png'

render_item = (item)->
  if item.meta and item.meta.author_name
    author_avatar = item.meta.author_avatar or default_avatar
    author_name = item.meta.author_name
    output_item_author = '
      <img src="'+author_avatar+'" alt="'+author_name+'"/>
      <h5>'+author_name+'</h5>
    '
  else
    output_item_author = '<h5>'+_('Anonymous')+'</h5>'
  if item.author
    remove_btn = '<a href="#" class="remove-comment">'+_('Remove')+'</a>'
  else
    remove_btn = ''

  output_item = '
  <div class="comm-item">
    <div class="author-container">
      '+output_item_author+'
    </div>
    <div class="comm-container">
      <p>'+item.content+'</p>
      '+remove_btn+'
    </div>
  </div>
  '
  return output_item


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
    output_comm_items += render_item(item)


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
        <textarea placeholder="'+_('Your Comment here...')+'"
                  rows="6"></textarea>
      </div>
      <button type="submit">
        '+_('Write your Comment')+'
      </button>
    </div>
  </form>
  <hr>
  <div class="comm-list">
    '+output_comm_items+'
  </div>
  '

if typeof SupExtComment isnt 'function'
  throw 'SupExtComment not fully loaded!!'

comment = new SupExtComment()

initHandler = ->

  # init locale
  setLocale(locale)

  # render elements
  comm_element = document.querySelector('#sup-comment-exts-plugin')
  if not comm_element
    return
  comm_element.innerHTML = render_list({}, [{author:true},{}])
  group_key = comm_element.getAttribute('group-key') or location.href

  comment.query({key: group_key})
  .then (comments)->
    author = comment.author.profile()
    comm_element.innerHTML = render_list(author, comments)

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