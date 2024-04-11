from atf.ui import *
from controls import *


@templatename("WorkTimeDocuments/timeoff:Dialog")
class Dialog(DocumentTemplate):

    employee_cl = ControlsLookupInput(By.CSS_SELECTOR, '[data-qa="staff-Lookup__input"]', 'Сотрудник')
    reason_re = RichEditorExtendedEditor()
    choose_date = Element(By.CSS_SELECTOR, '.wtd-TimeOff__MainTab-dateSelector', 'Выбор даты')
    date_window = ControlsCalendarPeriodDialog()
    phase_btn = Button(By.CSS_SELECTOR, '.edo3-PassageButton', 'Фаза документа')
    delete_btn = Button(By.CSS_SELECTOR, '[data-qa="deleteDocument"]', 'Удалить')
    confirm_window = ControlsPopupConfirmation()

    def fill_timeoff(self, **kwargs):
        """Заполнить отгул"""

        if 'Сотрудник' in kwargs.keys():
            self.employee_cl.autocomplete_search(kwargs['Сотрудник'])
        if 'Причина' in kwargs.keys():
            self.reason_re.type_in(kwargs['Причина'])

    def run_timeoff(self):
        """Оправить на выполнение"""

        self.phase_btn.click()
        self.phase_btn.should_not_be(ExactText('На выполнение'))
        self.phase_btn.should_be(ExactText('Согласовано'))

    def select_date(self, date):
        """Выбираем дату
        :param date: Дата в формате ДД.ММ.ГГ
        """

        self.choose_date.click()
        self.date_window.set_period(date)

    def check_timeoff(self, employee, reason, date):
        """Проверить отгул
        :param employee: Сотрудник
        :param reason: Причина отгула
        :param date: Дата отгула
        """

        self.employee_cl.should_be(ExactText(employee))
        self.reason_re.should_be(ExactText(reason))
        self.choose_date.should_be(ContainsText(date))

    def delete_timeoff(self):
        """Удалить отгул"""

        self.delete_btn.click()
        self.confirm_window.confirm()
