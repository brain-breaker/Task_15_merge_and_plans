from atf import log
from atf.ui import *
from controls import *


class Dialogs(Region):
    """Вкладка Диалоги в реестре Контакты"""

    folders = ControlsTreeGridView()
    messages_dialogs = ControlsListView(By.CSS_SELECTOR, '.msg-dialogs-detail .controls-ListViewV', 'Диалоги')
    messages_chats = ControlsListView(By.CSS_SELECTOR, '.msg-CorrespondenceDetail .controls-ListViewV', 'Чаты')
    tags = ControlsListView(By.CSS_SELECTOR, '.tags-list .controls-ListViewV', 'Теги')
    tag_name_message = Element(By.CSS_SELECTOR, '.tag-simple .tags-base__name', 'Тег на сообщении')
    close_tag = Element(By.CSS_SELECTOR, '.tags-base__close', 'Сброс тега')
    select_tag = ControlsListView(By.CSS_SELECTOR, '.msg-tags-aggregate__tags .controls-ListViewV', 'Выбор тега')
    move_window = ControlsMoveDialog()
    tabs = ControlsTabsButtons()

    def open_dialogs(self):
        """Открытие вкладки Диалоги"""

        log('Переходим во вкладку Диалоги в реестре Контакты')
        self.browser.open(self.config.get('SITE_DIALOGS'))
        self.check_page_load_wasaby()

    def check_load(self):
        """Проверка загрузки вкладки Диалоги"""

        self.folders.check_load()
        self.messages_dialogs.check_load()

    def move_message(self, message, folder):
        """Перемещение сообщения"""

        self.messages_dialogs.item(contains_text=message).select_menu_actions('Переместить', context_menu=True)
        self.move_window.select(contains_text=folder)

    def check_message(self, text):
        """Проверка сообщения по тексту"""

        self.messages_dialogs.item(contains_text=text).should_be(Displayed)

    def check_message_date(self, tab, message, date):
        """Проверяем дату сообщения во вкладке"""

        if tab == self.messages_dialogs:
            self.messages_dialogs.item(contains_text=message).should_be(ContainsText(date))
        elif tab == self.messages_chats:
            self.messages_chats.item(contains_text=message).should_be(ContainsText(date))

    def select_tab(self, tab):
        """Переключение по вкладкам"""

        self.tabs.select(tab)
        self.messages_chats.check_load()

    def put_or_drop_tag(self, message, tag):
        """Отметка сообщения тегом/Снятие тега с сообщения"""
        self.messages_dialogs.item(contains_text=message).select_menu_actions('Пометить', context_menu=True)
        self.select_tag.item(contains_text=tag).click()

    def check_tag_name_message(self, tag):
        """Проверка тега на сообщении"""

        self.tag_name_message.should_be(Displayed, ExactText(tag))
