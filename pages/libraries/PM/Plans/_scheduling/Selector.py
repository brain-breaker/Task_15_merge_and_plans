from atf.ui import *
from controls import *


@templatename("PM/Plans/_scheduling/Selector")
class Selector(StackTemplate):
    """
    Панель выбора
    PM/Plans/_scheduling/Selector
    """

    search = ControlsSearchInput()
    objects = ControlsTreeGridView()

    def select_object(self, planning_object):
        """Выбрать объект
        :param planning_object: объект планирования
        """

        self.search.search(planning_object, search_btn_click=True)
        self.objects.row(contains_text=planning_object).click()
