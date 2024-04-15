from atf.ui import *
from controls import *


@templatename("PM/Plans/dialog:Dialog")
class Dialog(StackTemplate):
    """Карточка плана работ"""

    object_cl = ControlsLookupInput()
    client_el = Element(By.CSS_SELECTOR, '[data-qa="edo3-Sticker__mainInfo"]', 'Заказчик')
    plan_point_btn = Button(By.CSS_SELECTOR, '[data-target="menu_item_point"]', 'Добавить пункт плана')
    phase_btn = Button(By.CSS_SELECTOR, '.edo3-PassageButton', 'На выполнение')
    plan_point_cl = ControlsTreeGridView()

    def add_object(self, planning_object):
        """Выбираем объект планирования через панель выбора
        :param planning_object: Объект планирования
        """

        from pages.libraries.PM.Plans._scheduling.Selector import Selector

        self.object_cl.open_btn.click()
        Selector(self.driver).select_object(planning_object)

    def select_client(self, client):
        """Выбираем заказчика
        :param client: Сотрудник
        """

        from pages.libraries.Addressee.popup import Stack

        self.client_el.click()
        Stack(self.driver).select(client)
        self.client_el.should_be(Displayed, ExactText(client))

    def add_plan_point(self, description, executor):
        """Добавляем пункт плана
        :param description: Описание
        :param executor: Исполнитель
        """

        from pages.libraries.PM.Plans.point import Dialog

        self.plan_point_btn.click()
        Dialog(self.driver).fill_point_plan(description, executor)

    def run_plan(self):
        """Оправить на выполнение"""

        self.phase_btn.click()
        self.phase_btn.should_not_be(ExactText('На выполнение'))

    def check_plan(self, planning_object, client, plan_point):
        """Проверить план работ
        :param planning_object: Объект планирования
        :param client: Заказчик
        :param plan_point: Пункт плана
        """

        self.object_cl.should_be(ExactText(planning_object))
        self.client_el.should_be(ExactText(client))
        self.plan_point_cl.should_be(ContainsText(plan_point))
