# -------------------------------
# Comment Extension Render.
# -------------------------------

default_avatar = 'styles/default_avatar.png'

_ = (text)->
  return text

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