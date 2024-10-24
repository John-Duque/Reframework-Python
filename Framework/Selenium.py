import logging
from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager


class Selenium:
    # Declaração de variáveis de instância com tipos
    logger: logging.Logger  # Logger para registro de logs
    driver: webdriver  # Driver do WebDriver

    def __init__(self, logger: logging.Logger, browser: str) -> None:
        self.driver = None  # Inicializa o driver como None para melhor controle de exceções
        self.logger = logger
        self.initialize_driver(browser)

    def initialize_driver(self, browser: str) -> None:
        # Inicializa o driver com base nas opções configuradas.
        try:
            match browser:
                case "chrome":
                    service = Service(ChromeDriverManager().install())
                    self.driver = webdriver.Chrome(service=service)
                case "firefox":
                    service = Service(GeckoDriverManager().install())
                    self.driver = webdriver.Firefox(service=service)
                case "edge":
                    service = Service(EdgeChromiumDriverManager().install())
                    self.driver = webdriver.Edge(service=service)
                case _:
                    raise ValueError(f"Navegador '{browser}' não é suportado.")

            # Maximiza a janela do navegador
            self.driver.maximize_window()
            self.logger.info(f"{browser.capitalize()} browser iniciado com sucesso.")
        except WebDriverException as e:
            self.logger.error(f"Erro ao iniciar o WebDriver: {str(e)}")
        except Exception as e:
            self.logger.error(f"Erro ao iniciar o WebDriver: {str(e)}")

    def get_driver(self) -> webdriver:
        # Retorna a instância do driver.
        if self.driver:
            return self.driver
        else:
            self.logger.error("Driver não está inicializado.")
            raise WebDriverException("Driver não foi inicializado corretamente.")

    def quit(self) -> None:
        # Fecha o navegador e trata exceções.
        try:
            if self.get_driver():
                self.driver.quit()
                self.logger.info("Navegador fechado com sucesso.")
            else:
                self.logger.warning("Tentativa de fechar um driver não inicializado.")
        except WebDriverException as e:
            self.logger.error(f"Erro ao fechar o navegador: {str(e)}")
        except Exception as e:
            self.logger.error(f"Erro ao fechar o navegador: {str(e)}")
