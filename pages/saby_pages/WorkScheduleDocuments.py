from atf import log
from atf.ui import *
from controls import *


class WorkScheduleDocuments(Region):
    """Реестр документов в графиках работ сотрудников"""

    create_btn = ExtControlsDropdownAddButton()
    documents = ControlsTreeGridView(By.CSS_SELECTOR, '[data-qa="wtd-List"] .controls-Grid', 'Документы')
    search = ControlsSearchInput()

    def open_ews_documents(self):
        """Открытие вкладки Документы в Графиках работ Сотрудников"""

        log('Переходим в Документы графиков работ сотрудников')
        self.browser.open(self.config.get('SITE_EWS_DOCUMENTS'))
        self.check_page_load_wasaby()

    def create_document(self, *regulation):
        """Создание документа

        :param regulation: подпункты меню
        """
        from pages.libraries.WorkTimeDocuments.timeoff import Dialog

        self.create_btn.select(*regulation)
        timeoff_card = Dialog(self.driver)
        timeoff_card.check_open()
        return timeoff_card

    def search_document(self, employee, reason):
        """Поиск документа
        :param employee: Сотрудник
        :param reason: Причина
        """

        self.search.search(employee, search_btn_click=True)
        self.documents.row(contains_text=reason).should_be(Displayed)

    def open_document(self, reason):
        """Открытие документа
        :param reason: Причина
        """

        self.documents.row(contains_text=reason).click()
