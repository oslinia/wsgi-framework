from framework.routing import callback, Error, Rule, Endpoint

from .endpoint import Handler, Index, Media, Query, Page, Redirect, Archive

Error(Handler)

Rule('/', 'index')
Endpoint('index', callback(Index))

Rule('/query', 'query')
Endpoint('query', callback(Query))

Rule('/media/{name}', 'media').where(
    name='[a-z]+[/.a-z]*'
)
Endpoint('media', callback(Media))

Rule('/page/{name}', 'page').where(
    name='[a-z]+[/.a-z]*'
)
Endpoint('page', callback(Page))

Rule('/redirect.html', 'redirect_index')
Endpoint('redirect_index', callback(Redirect, 'index'))

Rule('/redirect/{name}', 'redirect').where(
    name='[a-z]+[/.a-z]*'
)
Endpoint('redirect', callback(Redirect))

Rule('/archive/{year}', 'archive').where(year='[0-9]{4}')
Rule('/archive/{year}/{month}', 'archive')
Rule('/archive/{year}/{month}/{day}', 'archive').where(
    year='[0-9]{4}', month='[0-9]{1,2}', day='[0-9]{1,2}'
)
Endpoint('archive', callback(Archive))
