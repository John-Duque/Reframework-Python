import logging
from typing import List
from selenium.webdriver.remote.webdriver import WebDriver
from Components.google_page import GooglePage
from Framework.Exceptions import BusinessException


class ProcessTransaction:
    # Declaração de variáveis com tipos
    driver: WebDriver  # Driver WebDriver para controlar o navegador
    logger: logging.Logger  # Logger para registro de eventos
    google_page: GooglePage  # Página do Google para a automação

    def __init__(self, driver: WebDriver, logger: logging.Logger) -> None:
        # Injeção de dependência para a página.
        self.driver = driver
        self.logger = logger
        self.google_page = GooglePage(driver, logger)

    def execute(self, transaction: List[object]) -> None:
        for transaction in transaction:
            try:
                # Executa o processamento da transação com validações e tratamento de exceções.
                self.logger.info(f"Processando transação {transaction[0]}")
                self.google_page.open()
                self.google_page.search(transaction[1])
                self.logger.info(f" success {transaction[0]}")

            except BusinessException as e:
                self.logger.error(f"Erro de negócio na transação {transaction[0]}: {str(e)}")
                raise e  # Relança a exceção para ser tratada em outro nível

            except Exception as e:
                self.logger.error(f"Erro inesperado na transação {transaction['id']}: {str(e)}")
