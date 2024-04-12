from datetime import date
from atf import log, info
from atf.ui import *
from pages.AuthPage import AuthPage
from pages.saby_pages.WorkScheduleDocuments import WorkScheduleDocuments


class TestWorkScheduleDocuments(TestCaseUI):

    @classmethod
    def setUpClass(cls):
        cls.browser.open(cls.config.get('SITE'))
        AuthPage(cls.driver).auth(cls.config.get('USER_LOGIN'), cls.config.get('USER_PASSWORD'))
        cls.timeoff_page = WorkScheduleDocuments(cls.driver)
        # cls.tomorrow_date = (date.today() + timedelta(days=1)).strftime('%d.%m.%y')
        cls.tomorrow_date = date(2024, 4, 15).strftime('%d.%m.%y')

    def setUp(self):
        WorkScheduleDocuments(self.driver).open_ews_documents()

    def test_01_checking_timeoff(self):
        """ Создать отгул
            Выбрать сотрудника через автодополнение, которому создаем отгул
            Выставить дату - завтра
            Заполнить причину
            Запустить в ДО
            Убедиться, что появился в реестре и при переоткрытии значения в полях сохранились
            Удалить отгул"""

        timeoff_data = {'Сотрудник': 'Задач Автотест',
                        'Причина': 'Хочу порешать задачи из курса по автотестированию'}

        log('Создаем отгул')
        timeoff_card = self.timeoff_page.create_document('Отгул', 'Отгул (для тестов мобилки)')

        log('Заполняем необходимые данные в отгуле')
        timeoff_card.fill_timeoff(**timeoff_data)
        timeoff_card.select_date(self.tomorrow_date)

        log('Запускаем отгул в ДО')
        timeoff_card.run_timeoff()

        info('Закрываем карточку отгула после запуска в ДО')
        timeoff_card.close()

        log('Находим наш отгул')
        self.timeoff_page.search_document(*timeoff_data.values())

        log('Открываем отгул')
        self.timeoff_page.open_document(timeoff_data['Причина'])

        log('Проверяем отгул')
        timeoff_card.check_timeoff_by_date(*timeoff_data.values(), self.tomorrow_date)

        log('Удаляем отгул')
        timeoff_card.delete_timeoff()

    def test_02_checking_timeoff_from_directory(self):
        """ Создать отгул
            Выбрать сотрудника через справочник
            Выставить время завтра с 12 до 14 часов
            Заполнить описание
            Сохранить
            Убедиться, что появился в реестре и при переоткрытии значения в полях сохранились
            Удалить отгул"""

        timeoff_data = {'Сотрудник': 'Задач1 Автозакрытие1',
                        'Причина': 'Хочу посмотреть вебинары по автотестированию'}
        start_time = '12:00'
        end_time = '14:00'

        log('Создаем отгул')
        timeoff_card = self.timeoff_page.create_document('Отгул', 'Отгул (для тестов мобилки)')

        log('Заполняем необходимые данные в отгуле')
        timeoff_card.select_employee(timeoff_data['Сотрудник'])
        timeoff_card.fill_timeoff(Причина=timeoff_data['Причина'])
        timeoff_card.select_date(self.tomorrow_date)
        timeoff_card.select_time(start_time, end_time)

        log('Сохраняем отгул')
        timeoff_card.save_timeoff()

        log('Находим наш отгул')
        self.timeoff_page.search_document(*timeoff_data.values())

        log('Открываем отгул')
        self.timeoff_page.open_document(timeoff_data['Причина'])

        log('Проверяем отгул')
        timeoff_card.check_timeoff_by_time(*timeoff_data.values(), self.tomorrow_date, start_time, end_time)

        log('Удаляем отгул')
        timeoff_card.delete_timeoff()
