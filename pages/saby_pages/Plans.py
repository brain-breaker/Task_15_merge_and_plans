from atf import log
from atf.ui import *
from controls import *


class Plans(Region):
    """Реестр Планы работ"""

    create_btn = ExtControlsDropdownAddButton()
    plans = ControlsTreeGridView(By.CSS_SELECTOR, '.edo3-Browser .controls-Grid', 'Планы работ')
    search = ControlsSearchInput()
    popup_window = ControlsPopup()
    confirm_window = ControlsPopupConfirmation()

    def open_plans(self):
        """Открытие реестра"""

        log('Переходим в реестр Планы работ')
        self.browser.open(self.config.get('SITE_PLANS'))
        self.check_page_load_wasaby()

    def create_plan(self, *regulation):
        """Создание плана работ
        :param regulation: подпункты меню
        """
        from pages.libraries.PM.Plans.dialog import Dialog

        self.create_btn.select(*regulation)
        plan_card = Dialog(self.driver)
        plan_card.check_open()
        return plan_card

    def search_plan(self, planning_object, client):
        """Поиск плана работ
        :param planning_object: Объект планирования
        :param client: Заказчик
        """

        self.search.search(planning_object, search_btn_click=True)
        self.plans.row(contains_text=planning_object).should_be(Displayed, ContainsText(client))

    def open_plan(self, planning_object, client):
        """Открытие плана работ
        :param planning_object: Объект планирования
        :param client: Заказчик
        """

        self.plans.row(contains_text=planning_object).should_be(ContainsText(client)).click()

    def delete_plan(self, planning_object, client):
        """Удаление плана работ
        :param planning_object: Объект планирования
        :param client: Заказчик
        """

        self.plans.row(contains_text=planning_object).should_be(ContainsText(client)).open_context_menu()
        self.popup_window.select('Удалить')
        self.confirm_window.confirm()

    def check_should_not_be_plan(self, planning_object, client):
        """Проверка отсутствия плана работ
        :param planning_object: Объект планирования
        :param client: Заказчик
        """

        self.plans.should_not_be(Displayed, ContainsText(planning_object), ContainsText(client))
        self.search.clear()
        self.search.search(planning_object, search_btn_click=True)
        self.plans.check_rows_number(0)
