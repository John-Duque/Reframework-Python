import logging
from typing import Optional

from selenium.webdriver.remote.webdriver import WebDriver


class EndProcess:
    # Classe responsável por finalizar o processo com registro no log.

    logger: logging.Logger  # Logger para registrar eventos
    driver: WebDriver

    def __init__(self, driver: WebDriver,logger: logging.Logger) -> None:
        self.logger = logger
        self.driver = driver

    def finalize(self, message: Optional[str] = None) -> None:
        # Finaliza o processo com uma mensagem de log.
        try:
            if message:
                self.logger.info(f"Processo concluído: {message}")
                self.driver.quit()
            else:
                self.logger.info("Processo concluído com sucesso.")
                self.driver.quit()
        except Exception as e:
            self.logger.error(f"Erro ao finalizar o processo: {str(e)}")
