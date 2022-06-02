import tornado
from tornado.web import RequestHandler
import functools

# could also define get_login_url function (but must give up LoginHandler)
login_url = "/login"

users_list = {'user_1':'password_1', 'user_2': 'password_2', 'user_3': 'password_3'}

# could define get_user_async instead
def get_user(request_handler):
    return request_handler.get_cookie("user")

# optional login page for login_url
class LoginHandler(RequestHandler):
    def get(self):
        try:
            errormessage = self.get_argument("error")
        except Exception:
            errormessage = ""
        self.render("login.html", errormessage=errormessage)

    def check_permission(self, username, password):
        if username in users_list and users_list[username] == password:
            return True
        return False

    def post(self):
        username = self.get_argument("username", "")
        password = self.get_argument("password", "")
        auth = self.check_permission(username, password)
        if auth:
            self.set_current_user(username)
            self.redirect(self.get_argument("next", f"/{username}"))
        else:
            error_msg = "?error=" + tornado.escape.url_escape("Username or password is wrong, please try again.")
            self.redirect(login_url + error_msg)

    def set_current_user(self, user):
        if user:
            # self.set_secure_cookie("user_id", user["id"])
            self.set_cookie("user", tornado.escape.json_encode(user), expires_days=None)
        else:
            self.clear_cookie("user")

# This one of the method I have been trying to use to secure my routes
class YourDashboardHandler(RequestHandler):
    def get(self, *arg, **kwargs):
        user_from_URL = kwargs["user_id"]
        user_from_cookie = self.get_cookie("user", "")
        if user_from_URL != user_from_cookie:
            self.redirect(r"^/(?P<user_id>\w+)$")

# optional logout_url, available as curdoc().session_context.logout_url
logout_url = "/logout"

# optional logout handler for logout_url
class LogoutHandler(RequestHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", "/login"))

if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/login", LoginHandler),
        (r"^/(?P<user_id>\w+)$", YourDashboardHandler)
    ], cookie_secret="61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=")