from atf.ui import *
from controls import *
from pages.selectionNew import Stack


@templatename("WorkTimeDocuments/timeoff:Dialog")
class Dialog(DocumentTemplate):

    employee_cl = ControlsLookupInput(By.CSS_SELECTOR, '[data-qa="staff-Lookup__input"]', 'Сотрудник', catalog=Stack)
    reason_re = RichEditorExtendedEditor()
    choose_date = Element(By.CSS_SELECTOR, '.wtd-TimeOff__MainTab-dateSelector', 'Выбор даты')
    choose_time = Element(By.CSS_SELECTOR, '[data-name="dayTimeSelector_timeButton"]', 'Выбор времени')
    start_time_tf = TextField(By.CSS_SELECTOR, '[data-qa="wtd-TimeIntervalMinutes__start"] input', 'Время начала')
    end_time_tf = TextField(By.CSS_SELECTOR, '[data-qa="wtd-TimeIntervalMinutes__end"] input', 'Время окончания')
    date_tf = TextField(By.CSS_SELECTOR, '[data-qa="wtd-DayTimeSelector__dateInput"] input', 'Дата')
    date_window = ControlsCalendarPeriodDialog()
    phase_btn = Button(By.CSS_SELECTOR, '.edo3-PassageButton', 'Фаза документа')
    delete_btn = Button(By.CSS_SELECTOR, '[data-qa="deleteDocument"]', 'Удалить')
    save_btn = Button(By.CSS_SELECTOR, '[data-qa="edo3-ReadOnlyStateTemplate__saveButton"]', 'Сохранить')
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

    def save_timeoff(self):
        """Сохранить отгул"""

        self.save_btn.click()

    def select_date(self, date):
        """Выбираем дату
        :param date: Дата в формате ДД.ММ.ГГ
        """

        self.choose_date.click()
        self.date_window.set_period(date)

    def select_time(self, start_time, end_time):
        """Выбираем время
        :param start_time: время начала отгула в формате 'ЧЧ:ММ'
        :param end_time: время окончания отгула в формате 'ЧЧ:ММ'
        """

        start_time_str = ''.join(start_time.split(':'))
        end_time_str = ''.join(end_time.split(':'))

        self.choose_time.click()
        self.start_time_tf.set_absolute_position()
        self.start_time_tf.human_type_in(start_time_str)
        self.end_time_tf.set_absolute_position()
        self.end_time_tf.human_type_in(end_time_str)

    def select_employee(self, employee):
        """Выбираем сотрудника
        :param employee: Сотрудник
        """

        self.employee_cl.click().select(employee)
        self.employee_cl.should_be(Displayed)

    def check_timeoff_by_date(self, employee, reason, date):
        """Проверить отгул по дате
        :param employee: Сотрудник
        :param reason: Причина отгула
        :param date: Дата отгула
        """

        self.employee_cl.should_be(ExactText(employee))
        self.reason_re.should_be(ExactText(reason))
        self.choose_date.should_be(ContainsText(date))

    def check_timeoff_by_time(self, employee, reason, date, start_time, end_time):
        """Проверить отгул по времени отгула
        :param employee: Сотрудник
        :param reason: Причина отгула
        :param date: Дата отгула
        :param end_time: Время начала отгула в формате строки 'ЧЧ:ММ'
        :param start_time: Время окончания отгула в формате строки 'ЧЧ:ММ'
        """

        self.employee_cl.should_be(ExactText(employee))
        self.reason_re.should_be(ExactText(reason))
        self.date_tf.should_be(Attribute(value=date))
        self.start_time_tf.should_be(Attribute(value=start_time))
        self.end_time_tf.should_be(Attribute(value=end_time))

    def delete_timeoff(self):
        """Удалить отгул"""

        self.delete_btn.click()
        self.confirm_window.confirm()
