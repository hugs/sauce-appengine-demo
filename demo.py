from vendor import web
from StringIO import StringIO
from saucetest import TestSauceWithAppEngine
import basicauth
import unittest
import logging
import settings

urls = (
  '/', 'hello',
  '/test', 'test'
)


def basic_credentials(username, password, realm):
    return (username == settings.basic_auth_name and 
            password == settings.basic_auth_password) 

authorize = basicauth.auth(verify = basic_credentials, 
                           realm="Sauce Labs - AppEngine") 

render = web.template.render('templates', base='base')

class hello:
    def GET(self):
        return render.hello()

class test:
    @authorize
    def GET(self):
        suite = unittest.makeSuite(TestSauceWithAppEngine)
        log_stream = StringIO()
        rs = unittest.TextTestRunner(stream=log_stream, verbosity=2).run(suite)
        return render.test("%s" % log_stream.getvalue())

app = web.application(urls, globals())
main = app.cgirun()
