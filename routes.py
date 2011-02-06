routes_in = (
  ('/', '/welcome/default/index'),
  ('/$f', '/welcome/default/$f'),
  ('/user/$f', '/welcome/default/user/$f'),
  ('/static/(?P<any>.*)', '/welcome/static/\g<any>'),
)

routes_out = (
  ('/welcome/default/index','/'),
  ('/welcome/default/$f','/$f'),
  ('/welcome/default/user/$f','/user/$f'),
  ('/welcome/static/$a/$b/$c', '/static/$a/$b/$c'),
  ('/welcome/static/\g<any>','/static/(?P<any>.*)'),
)