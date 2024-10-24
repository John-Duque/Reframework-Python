import json
import logging
import os
from typing import Dict, Any


class Init:
    # Declaração das variáveis e seus tipos
    config_path: str  # Caminho do arquivo de configuração
    config: Dict[str, Any]  # Dicionário com as configurações carregadas
    logger: logging.Logger  # Logger para registro de logs

    def __init__(self, config_path: str = 'Data/config.json') -> None:
        # Inicializa a classe e carrega as configurações do arquivo JSON.
        self.config_path = config_path
        self.config = self.load_config()
        self.logger = self.setup_logger()

    def load_config(self) -> Dict[str, Any]:
        # Carrega as configurações do JSON e trata exceções.
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Configuração não encontrada: {self.config_path}")

        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Erro ao carregar o JSON: {e}")

    def setup_logger(self) -> logging.Logger:
        # Configura o logger com base nas configurações.
        log_file = self.config["Settings"]["LogFile"]

        try:
            logging.basicConfig(
                filename=log_file,
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s'
            )
            return logging.getLogger()
        except Exception as e:
            raise RuntimeError(f"Erro ao configurar o logger: {e}")

    def get_config(self) -> Dict[str, Any]:
        # Retorna a configuração carregada.
        return self.config

    def get_logger(self) -> logging.Logger:
        # Retorna o logger configurado.
        return self.logger
