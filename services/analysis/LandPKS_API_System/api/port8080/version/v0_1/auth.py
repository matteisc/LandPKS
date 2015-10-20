import cherrypy
import json
from database_layer import LandPKS_Database_Driver
SESSION_KEY = '_cp_username'
def check_credentials(username, password):
    if LandPKS_Database_Driver.check_auth_api_account(username,password) == 1:
        return None
    else:
        return u"Incorrect username or password."
def check_auth(*args, **kwargs):
    conditions = cherrypy.request.config.get('auth.require', None)
    if conditions is not None:
        username = cherrypy.session.get(SESSION_KEY)
        if username:
            cherrypy.request.login = username
            for condition in conditions:
                # A condition is just a callable that returns true or false
                if not condition():
                    raise cherrypy.HTTPRedirect("/auth/login")
        else:
            raise cherrypy.HTTPRedirect("/auth/login")
    
cherrypy.tools.auth = cherrypy.Tool('before_handler', check_auth)

def require(*conditions):
    """A decorator that appends conditions to the auth.require config
    variable."""
    def decorate(f):
        if not hasattr(f, '_cp_config'):
            f._cp_config = dict()
        if 'auth.require' not in f._cp_config:
            f._cp_config['auth.require'] = []
        f._cp_config['auth.require'].extend(conditions)
        return f
    return decorate

def member_of(groupname):
    def check():
        # replace with actual check if <username> is in <groupname>
        return cherrypy.request.login == 'joe' and groupname == 'admin'
    return check

def name_is(reqd_username):
    return lambda: reqd_username == cherrypy.request.login

def any_of(*conditions):
    """Returns True if any of the conditions match"""
    def check():
        for c in conditions:
            if c():
                return True
        return False
    return check

# By default all conditions are required, but this might still be
# needed if you want to use it inside of an any_of(...) condition
def all_of(*conditions):
    """Returns True if all of the conditions match"""
    def check():
        for c in conditions:
            if not c():
                return False
        return True
    return check

def return_response_error(code,type,mess,format="JSON"):
    if (format=="JSON"):
        cherrypy.response.headers['Content-Type'] = "application/json"
        cherrypy.response.headers['Retry-After']=60
        cherrypy.response.status = code
        message = {type:mess}
        return json.dumps(message)
    else:
        return "Not support yet"

# Controller to provide login and logout actions

class AuthController(object):
    
    def on_login(self, username):
        """Called on successful login"""
        print "Exporting LandPKS Dat file for client"
        
    
    def on_logout(self, username):
        """Called on logout"""
    
    def get_loginform(self, username, msg="LandPKS Authentication", from_page="/"):
        return """<html><body align="center">
            <form method="post" action="/auth/login">
            <input type="hidden" name="from_page" value="%(from_page)s" />
            %(msg)s<br/><br/>
            Username: <input type="text" name="username" value="%(username)s" /><br />
            Password: <input type="password" name="password" /><br /><br />
            <input type="submit" value="Log in" />
        </body></html>""" % locals()
    
    @cherrypy.expose
    def login(self, username=None, password=None, from_page="/"):
        if username is None or password is None:
            return self.get_loginform("", from_page=from_page)
        error_msg = check_credentials(username, password)
        if error_msg:
            return self.get_loginform(username, error_msg, from_page)
        else:
            cherrypy.session[SESSION_KEY] = cherrypy.request.login = username
            self.on_login(username)
            cookie = cherrypy.response.cookie
            cherrypy.response.headers['Content-Type'] = "application/json"
            cherrypy.response.headers['Retry-After']=60
            cherrypy.response.status = 200
            
            if (str(cookie)[0:11].strip().upper() == "SET-COOKIE:"):
               str_cookie = str(cookie)[11:].strip()
            else:
               str_cookie = str(cookie).strip()  
            message = {'auth_key':str_cookie}
            return json.dumps(message)
        
        
    @cherrypy.expose
    def api_login(self, **request_data):
        print request_data
        try:
            email = str(request_data['email']).strip();
        except:
            return return_response_error(401,'error','Missing email ID',format="JSON")
        
        try:
            password = str(request_data['password']).strip();
        except:
            return return_response_error(401,'error','Missing password',format="JSON")
        
        username = LandPKS_Database_Driver.get_username_from_input(email)
        print "Find username : " + username
        if username is None or password is None:
            return return_response_error(401,'error','Missing authentication',format="JSON")
        error_msg = check_credentials(username, password)
        if error_msg:
            #return self.get_loginform(username, error_msg, from_page)
            return return_response_error(401,'error',error_msg,format="JSON")
        else:
            cherrypy.session[SESSION_KEY] = cherrypy.request.login = username
            self.on_login(username)
            cookie = cherrypy.response.cookie
            cherrypy.response.headers['Content-Type'] = "application/json"
            cherrypy.response.headers['Retry-After']=60
            cherrypy.response.status = 200
            
            if (str(cookie)[0:11].strip().upper() == "SET-COOKIE:"):
               str_cookie = str(cookie)[11:].strip()
            else:
               str_cookie = str(cookie).strip()  
            message = {'auth_key':str_cookie}
            return json.dumps(message)
        
        
    @cherrypy.expose
    def logout(self, from_page="/"):
        sess = cherrypy.session
        username = sess.get(SESSION_KEY, None)
        sess[SESSION_KEY] = None
        if username:
            cherrypy.request.login = None
            self.on_logout(username)
        raise cherrypy.HTTPRedirect(from_page or "/")
