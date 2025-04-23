from bootstrap.http.routing import callback, Error, Rule, Endpoint

from .controller import Handler, Page, Redirect, Archive

Error(Handler)

Rule('/', 'index')
Endpoint('index', callback(Page, 'index'))

Rule('/query', 'query')
Endpoint('query', callback(Page, 'url'))

Rule('/static/{name}', 'static').where(name='[a-z]+[/.a-z]*')
Endpoint('static', callback(Page, 'static'))

Rule('/page/{name}', 'page').where(name='[a-z]+[.a-z]*')
Endpoint('page', callback(Page))

Rule('/redirect', 'redirect_index')
Endpoint('redirect_index', callback(Redirect, 'index'))

Rule('/redirect/{name}', 'redirect').where(name='[a-z]+[.a-z]*')
Endpoint('redirect', callback(Redirect))

Rule('/archive/{year}', 'archive').where(year='[0-9]{4}')
Rule('/archive/{year}/{month}', 'archive')
Rule('/archive/{year}/{month}/{day}', 'archive').where(
    year='[0-9]{4}', month='[0-9]{1,2}', day='[0-9]{1,2}'
)
Endpoint('archive', callback(Archive))
