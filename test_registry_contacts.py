from atf import log
from atf.ui import *
from pages.auth_page import AuthPage
from pages.contacts_page import ContactsRegistry


class TestRegistryContacts(TestCaseUI):

    @classmethod
    def setUpClass(cls):
        cls.browser.open(cls.config.get('SITE'))
        AuthPage(cls.driver).auth(cls.config.get('USER_LOGIN'), cls.config.get('USER_PASSWORD'))
        cls.page = ContactsRegistry(cls.driver)
        cls.message = cls.config.get('USER_MESSAGE')
        cls.root = cls.config.get('MESSAGES_ROOT')

    def setUp(self):
        ContactsRegistry(self.driver).open_contacts()
        self.page.check_load()

    def test_01_checking_movement(self):

        folder = 'Папка для перемещения'

        log('Перейти в папку. '
            'Проверить количество диалогов в папке, папка должна быть пустая')
        self.page.folders.row(contains_text=folder).click()
        self.page.messages_dialogs.check_size(0)
        self.page.folders.row(contains_text=self.root).click()

        log('Перемещение сообщения')
        self.page.move_message(self.message, folder)

        log('Перейти в папку. '
            'Проверить сообщение в папке, а также количество: в папке должно быть 1 сообщение')
        self.page.folders.row(contains_text=folder).click()
        self.page.check_message(self.message)
        self.page.messages_dialogs.check_size(1)

        log('Вернуть сообщение обратно в корень. '
            'Проверяем, что папка снова пустая')
        self.page.move_message(self.message, self.root)
        self.page.messages_dialogs.check_size(0)

    def test_02_checking_message_date(self):

        date = '8 апр 12:56'

        log('Проверить дату сообщения в реестре Диалоги')
        self.page.check_message_date(self.page.messages_dialogs, self.message, date)

        log('Переключиться на вкладку')
        self.page.select_tab('Чаты')

        log('Проверить дату сообщения в Чатах')
        self.page.check_message_date(self.page.messages_chats, self.message, date)

    def test_03_checking_tag_message(self):

        tag = 'Тег для автотеста'

        log('Перейти в папку с тегом. '
            'Проверить количество диалогов в папке с тегом, папка должна быть пустая')
        self.page.tags.item(contains_text=tag).click()
        self.page.messages_dialogs.check_size(0)
        self.page.close_tag.click()

        log('Пометить сообщение эталонным тегом')
        self.page.put_or_drop_tag(self.message, tag)

        log('Проверить, что тег появился на сообщении, а в папке с тегом должно быть 1 сообщение')
        self.page.check_tag_name_message(tag)
        self.page.tags.item(contains_text=tag).click()
        self.page.messages_dialogs.check_size(1)

        log('Снять тег. '
            'Проверить, что папка с тегом снова пустая')
        self.page.put_or_drop_tag(self.message, tag)
        self.page.messages_dialogs.check_size(0)
