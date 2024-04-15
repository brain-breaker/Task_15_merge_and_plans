from atf.ui import *
from controls import *


@templatename("PM/Plans/point:Dialog")
class Dialog(DialogTemplate):
    """Карточка пункта плана"""

    desc_tf = ControlsInputArea()
    executor_btn = Button(By.CSS_SELECTOR, '.plan-PointImplementers__addBtn', 'Исполнитель')
    save_btn = Button(By.CSS_SELECTOR, '[data-qa="edo3-ReadOnlyStateTemplate__saveButton"]', 'Сохранить')

    def fill_point_plan(self, description, executor):
        """Заполняем пункт плана
        :param description: Описание
        :param executor: Исполнитель
        """

        from pages.libraries.Staff.selectionNew import Stack

        self.desc_tf.should_be(Displayed).type_in(description)
        self.executor_btn.click()
        Stack(self.driver).select(executor)
        self.save_btn.click()
