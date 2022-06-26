from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class ConsultaPage(BasePage):
    _search_input = {'by': By.ID, 'value': 'search'}
    _search_button = {'by': By.CLASS_NAME, 'value': 'button-search'}
    _search_text = {'by': By.CLASS_NAME, 'value': 'product-title'}
    _get_text = {'by': By.NAME, 'value': 'h1'}

    def __int__(self, driver):
        # instanciando o Selenium
        self.driver = driver

    def buscar_(self, search):
        self._entrar('busca')
        self._escrever(self._search_input, search)
        self._clicar(self._search_button)

    def pesquisar(self):
        return self._aparecer(self._search_text, 10)

    # def encontrartext(self):
    # return self._encontrartext(self._get_text)
