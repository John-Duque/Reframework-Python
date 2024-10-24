import logging
from typing import Tuple

from selenium.webdriver.remote.webdriver import WebDriver

from Framework.BasePage import BasePage


class GooglePage(BasePage):
    # Declaração das variáveis de instância com tipos
    driver: WebDriver  # Driver do WebDriver para controle do navegador
    search_box: Tuple[str, str]  # Localizador para a caixa de pesquisa

    def __init__(self, driver: WebDriver, logger: logging.Logger) -> None:
        super().__init__(driver, logger)
        self.driver = driver  # Inicializa o driver
        self.search_box = ("name", "q")  # Define o localizador da caixa de pesquisa

    def open(self) -> None:
        self.driver.get("https://www.google.com")

    def search(self, query: str) -> None:
        self.enter_text(*self.search_box, query)
        self.find_element(*self.search_box).submit()
