import logging
from functools import lru_cache
from typing import Dict, Any, Optional

import requests
from requests import Response


class HttpClient:
    base_url: str  # URL base para as requisições
    token: Optional[str]  # Token de autenticação Bearer
    headers: Dict[str, str]  # Cabeçalhos HTTP padrão para todas as requisições
    timeout: int  # Tempo limite para as requisições, em segundos
    max_retries: int  # Número máximo de tentativas em caso de falha temporária
    enable_cache: bool  # Se True, ativa o cache para requisições GET
    logger: logging.Logger  # Logger para monitoramento
    config: Dict[str, Any]  # config Dicionário com as configurações do arquivo config.json.

    def __init__(self, config: Dict[str, Any], logger: logging.Logger) -> None:
        # Inicializa o HttpClient com configurações do arquivo config.json.
        self.config = config
        # Configuração base extraída do config.json
        self.base_url = self.config["Settings"]["HttpClient"]["BaseUrl"].rstrip('/')
        self.timeout = self.config["Settings"]["HttpClient"]["Timeout"]
        self.max_retries = self.config["Settings"]["HttpClient"]["MaxRetries"]
        self.enable_cache = self.config["Settings"]["HttpClient"]["EnableCache"]

        # Configura o logger
        self.logger = logger

        # Configuração de cabeçalhos padrão e token de autenticação
        self.headers = config["Settings"]["HttpClient"]["Headers"]

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Optional[Response]:
        # Realiza uma requisição HTTP com retentativas em caso de falhas temporárias.

        # endpoint (str): Endpoint da API.

        # Optional[Response]: Objeto Response ou None em caso de erro.
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        attempt = 0
        while attempt < self.max_retries:
            try:
                response = requests.request(method, url, headers=self.headers, timeout=self.timeout, **kwargs)
                response.raise_for_status()
                self.logger.info(f"{method} {url} - Sucesso")
                return response
            except requests.exceptions.RequestException as e:
                self.logger.error(f"{method} {url} - Tentativa {attempt + 1} falhou: {e}")
                attempt += 1
        return None

    @lru_cache(maxsize=128)
    def _cached_get(self, endpoint: str, **kwargs) -> Optional[Dict[str, Any]]:
        # Requisição GET com cache, habilitado se enable_cache for True.
        response = self._make_request("GET", endpoint, **kwargs)
        return response.json() if response else None

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        # Executa uma requisição GET, com cache opcional se habilitado.
        if self.enable_cache:
            return self._cached_get(endpoint, params=params)
        else:
            response = self._make_request("GET", endpoint, params=params)
            if response:
                return response.json()
            else:
                return None

    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None) -> \
            Optional[Dict[str, Any]]:
        # Executa uma requisição POST.
        response = self._make_request("POST", endpoint, data=data, json=json)
        if response:
            return response.json()
        else:
            return None

    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        # Executa uma requisição PUT.
        response = self._make_request("PUT", endpoint, data=data)
        if response:
            return response.json()
        else:
            return None

    def delete(self, endpoint: str) -> bool:
        # Executa uma requisição DELETE.
        response = self._make_request("DELETE", endpoint)
        if response:
            return True
        else:
            return False
