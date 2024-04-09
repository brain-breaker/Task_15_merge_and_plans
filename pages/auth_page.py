from atf.ui import *


class AuthPage(Region):

    login = TextField(By.CSS_SELECTOR, '[type="text"]', 'логин')
    password = TextField(By.CSS_SELECTOR, '[type="password"]', 'пароль')

    def auth(self, login: str, password: str):
        """Авторизация"""

        self.browser.open(self.config.get('SITE_CONTACTS'))
        self.login.type_in(login + Keys.ENTER)
        self.login.should_be(ExactText(login))
        self.password.type_in(password + Keys.ENTER)
