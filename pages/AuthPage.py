from atf import info
from atf.ui import *


class AuthPage(Region):

    login = TextField(By.CSS_SELECTOR, '[type="text"]', 'логин')
    password = TextField(By.CSS_SELECTOR, '[type="password"]', 'пароль')

    def auth(self, user_login, user_password):
        """
        Авторизация на онлайн
        :param user_login: Логин
        :param user_password: Пароль
        """

        info(f'Авторизуемся на онлайне под пользователем {user_login}')
        self.login.type_in(user_login + Keys.ENTER)
        self.login.should_be(ExactText(user_login))
        self.password.type_in(user_password + Keys.ENTER)
        self.password.should_not_be(Displayed, wait_time=True)
        self.check_page_load_wasaby()
