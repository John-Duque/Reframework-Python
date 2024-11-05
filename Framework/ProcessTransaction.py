import logging

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

    def execute(self, transaction: object) -> None:
        try:
            # Executa o processamento da transação com validações e tratamento de exceções.
            self.logger.info(f"Processando transação {transaction}")
            self.google_page.open()
            self.logger.info(f" success {transaction}")

        except BusinessException as e:
            self.logger.error(f"Erro de negócio na transação {transaction}: {str(e)}")
            raise e  # Relança a exceção para ser tratada em outro nível

        except Exception as e:
            self.logger.error(f"Erro inesperado na transação {transaction}: {str(e)}")
