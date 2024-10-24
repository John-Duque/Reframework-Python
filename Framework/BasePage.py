import logging
from typing import Optional
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException


class BasePage:
    driver: WebDriver  # Variável de instância com type hint
    timeout: int  # Variável de instância com type hint
    logger: logging.Logger  # Variável de instância com type hint

    def __init__(self, driver: WebDriver, logger: logging.Logger, timeout: int = 10) -> None:
        # Inicializa a página base com o driver e o tempo de espera padrão.
        self.driver = driver
        self.timeout = timeout
        self.logger = logger

    def wait_until(self, condition, by: str, value: str, timeout: Optional[int] = None) -> Optional[WebElement]:
        # Espera explícita genérica que aguarda até que a condição fornecida seja atendida.
        try:
            return WebDriverWait(self.driver, timeout or self.timeout).until(
                condition((by, value))
            )
        except TimeoutException:
            self.logger.warning(f"Timeout: O elemento com {by}='{value}' não foi encontrado.")
            return None
        except NoSuchElementException:
            self.logger.error(f"Erro: O elemento com {by}='{value}' não foi encontrado no DOM.")
            return None

    def find_element(self, by: str, value: str, timeout: Optional[int] = None) -> Optional[WebElement]:
        # Localiza um elemento na página com espera explícita.
        return self.wait_until(ec.presence_of_element_located, by, value, timeout)

    def wait_for_visibility(self, by: str, value: str, timeout: Optional[int] = None) -> Optional[WebElement]:
        # Aguarda até que o elemento esteja visível.
        return self.wait_until(ec.visibility_of_element_located, by, value, timeout)

    def click(self, by: str, value: str) -> None:
        # Localiza um elemento e clica nele.
        try:
            element = self.find_element(by, value)
            if element:
                element.click()
                self.logger.info(f"Elemento com {by}='{value}' clicado com sucesso.")
            else:
                self.logger.warning(f"Elemento com {by}='{value}' não encontrado para clicar.")
        except ElementNotInteractableException:
            self.logger.error(f"Elemento com {by}='{value}' não está interagível.")

    def enter_text(self, by: str, value: str, text: str) -> None:
        # Localiza um campo de texto, limpa-o e insere o texto fornecido.
        try:
            element = self.find_element(by, value)
            if element:
                element.clear()
                element.send_keys(text)
                self.logger.info(f"Texto inserido com sucesso no elemento {by}='{value}'.")
            else:
                self.logger.warning(f"Elemento com {by}='{value}' não encontrado para inserir texto.")
        except ElementNotInteractableException:
            self.logger.error(f"Não foi possível interagir com o elemento {by}='{value}' para inserir texto.")
