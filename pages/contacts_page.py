from atf.ui import *
from controls import *


class ContactsRegistry(Region):
    """Реестр Контакты"""

    folders = ControlsTreeGridView()
    messages_dialogs = ControlsListView(By.CSS_SELECTOR, '.msg-dialogs-detail .controls-ListViewV', 'Диалоги')
    messages_chats = ControlsListView(By.CSS_SELECTOR, '.msg-CorrespondenceDetail .controls-ListViewV', 'Чаты')
    move_window = ControlsMoveDialog()
    tabs = ControlsTabsButtons()

    def check_load(self):
        """Проверка загрузки реестра"""

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
