from atf import *
from atf.ui import *
from pages.auth_page import AuthPage
from pages.contacts_page import ContactsRegistry


class TestRegistryContacts(TestCaseUI):

    @classmethod
    def setUpClass(cls):
        AuthPage(cls.driver).auth(cls.config.get('USER_LOGIN'), cls.config.get('USER_PASSWORD'))
        cls.page = ContactsRegistry(cls.driver)
        cls.message = cls.config.get('USER_MESSAGE')

    def setUp(self):
        self.browser.open(self.config.get('SITE_CONTACTS'))
        self.page.check_load()

    def test_01_checking_movement(self):

        folder = 'Папка для перемещения'
        root = 'Все сообщения'

        log('Перейти в папку. '
            'Проверить количество диалогов в папке, папка должна быть пустая')
        self.page.folders.row(contains_text=folder).click()
        self.page.messages_dialogs.check_size(0)
        self.page.folders.row(contains_text=root).click()

        log('Перемещение сообщения')
        self.page.move_message(self.message, folder)

        log('Перейти в папку. '
            'Проверить сообщение в папке, а также количество: в папке должно быть 1 сообщение')
        self.page.folders.row(contains_text=folder).click()
        self.page.check_message(self.message)
        self.page.messages_dialogs.check_size(1)

        log('Вернуть сообщение обратно в корень. '
            'Проверяем, что папка снова пустая')
        self.page.move_message(self.message, root)
        self.page.messages_dialogs.check_size(0)

    def test_02_checking_message_date(self):

        date = '8 апр 12:56'

        log('Проверить дату сообщения в реестре Диалоги')
        self.page.check_message_date(self.page.messages_dialogs, self.message, date)

        log('Переключиться на вкладку')
        self.page.select_tab('Чаты')

        log('Проверить дату сообщения в Чатах')
        self.page.check_message_date(self.page.messages_chats, self.message, date)
