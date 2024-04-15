from atf import log, info
from atf.ui import *
from pages.AuthPage import AuthPage
from pages.saby_pages.Plans import Plans


class TestPlans(TestCaseUI):

    @classmethod
    def setUpClass(cls):
        cls.browser.open(cls.config.get('SITE'))
        AuthPage(cls.driver).auth(cls.config.get('USER_LOGIN'), cls.config.get('USER_PASSWORD'))
        cls.plan_page = Plans(cls.driver)

    def setUp(self):
        Plans(self.driver).open_plans()

    def test_01_checking_plan(self):
        """ Создайте план работ
            Выберите объект планирования через панель выбора
            Укажите заказчика
            Добавьте пункт плана, указав описание и исполнителя
            Запустите план в документооборот
            Откройте созданный план и убедитесь,
            что пункт плана, заказчик и исполнитель отображаются согласно введенным ранее данным
            Удалите созданный план через реестр
            Убедитесь, что план не отображается в реестре."""

        planning_object = 'Задач Автотест Юрьевич'
        client = 'Задач Автотест'
        desc_point_plan = 'Делаем 15 задание'
        executor = 'Счётчик Задач'

        log('Создаем план работ')
        plan_card = self.plan_page.create_plan('План работ')

        log('Выбираем объект планирования через панель выбора')
        plan_card.add_object(planning_object)

        log('Указываем заказчика')
        plan_card.select_client(client)

        log('Добавляем пункт плана, указав описание и исполнителя')
        plan_card.add_plan_point(desc_point_plan, executor)

        log('Запускаем план в документооборот')
        plan_card.run_plan()

        info('Находим в реестре созданный план')
        self.plan_page.search_plan(planning_object, client)

        log('Открываем созданный план')
        self.plan_page.open_plan(planning_object, client)

        log('Проверяем, что пункт плана, заказчик '
            'и исполнитель (объект планирования) отображаются согласно введенным ранее данным')
        plan_card.check_plan(planning_object, client, desc_point_plan)

        info('Закрываем план работ')
        plan_card.close()

        log('Удаляем созданный план через реестр')
        self.plan_page.delete_plan(planning_object, client)

        log('Проверяем, что план не отображается в реестре')
        self.plan_page.check_should_not_be_plan(planning_object, client)
