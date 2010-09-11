#  http://basicauth.jottit.com/
#  By Josh Goldoot
#  Public domain.
#  Version 0.1
#  This creates a decorator that lets you require HTTP basic authentication
#    in a web.py app.

# Sample usage (modifying the classic "Hello, world!"):
##    import web
##    import basicauth
##    
##    def myVerifier(username, password, realm):
##        return (username == "falken" and password == "joshua") \
##            or (username == "lightman" and password == "pencil")
##        # (obviously you want something better in the real world...)
##    
##    auth = basicauth.auth(verify = myVerifier) 
##    
##    urls = ( '/(.*)', 'hello' )
##    
##    class hello:
##        @auth
##        def GET(self, name):
##            i = web.input(times=1)
##            if not name: name = basicauth.authUserName() # The name passed in the headers
##            for c in xrange(int(i.times)): 
##                print 'Hello,', web.websafe(name)+'!'
##    
##    web.run(urls, globals())

from vendor import web
from base64 import b64decode

# Default is NO valid user names or passwords.
# Remember not to store plaintext passwords on your server!   
authPasswordDictionary = {     }

def defaultDeny(realm, remoteUser, remotePassword, redirectURL):
    #print "Access denied!"
    pass

def dictVerify(remoteUser, remotePassword, realm=None):
    """The 'default' Inputs: the username and password entered by the user, and the realm for authentication.
    Return true if and only if the password is correct for the user name."""
    correctPassword = authPasswordDictionary.get(remoteUser, None)
    return correctPassword and remotePassword and remotePassword == correctPassword

def authUserName():
    """Returns the HTTP username passed in the request headers, or 'None' if none."""
    return web.ctx.get('environ',{}).get('REMOTE_USER', None)

def auth(verify = dictVerify, realm = "Protected", notAuthenticatedFunc = defaultDeny, redirectURL="/"):
    """Allows a function or method to be called only if the user authenticates.  Arguments:
        verify:  a function that returns true if the username and password are correct for this realm.
        realm: a string naming the security "realm."
        notAuthenticatedFunc: a function to call if the user clicks "Cancel" on his browser's box.

        To save typing, toward the top of your code put something like:
        myauth = basicauth.auth(verify = myVerifyFunction, realm="MySite")
        Then just put @myauth on a line before each method you want to protect.
        """
    def decorator(func, *args, **keywords):
        def f(*args, **keywords):
            remotePassword = None
            remoteUser = None
            try:
                b64text = web.ctx.env['HTTP_AUTHORIZATION'][6:]
                plainText = b64decode(b64text)
                remoteUser, remotePassword = plainText.split(':')
            except:
                pass

            if remoteUser and remotePassword and verify(remoteUser, remotePassword, realm):
                return func(*args, **keywords)
            else:
                web.ctx.status = "401 UNAUTHORIZED"
                web.header("WWW-Authenticate", 'Basic realm="%s"'  % web.websafe(realm) )
                return notAuthenticatedFunc(realm, remoteUser, remotePassword, redirectURL)
        return f
    return decorator
