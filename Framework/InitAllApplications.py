import logging
from typing import List, Any, Dict

from selenium.webdriver.remote.webdriver import WebDriver


class InitAllApplications:
    # Declaração de variáveis de instância com tipos
    logger: logging.Logger
    driver: WebDriver
    config: Dict[str,Any]
    transactionData: List[object]

    def __init__(self, driver: WebDriver, logger: logging.Logger, config: Dict[str,Any]) -> None:
        # Inicializa a classe com uma lista genérica de objetos.
        self.driver = driver
        self.logger = logger
        self.config = config

    def work(self) -> List[object]:
        # Retorna todos os objetos da lista.
        return self.transactionData
