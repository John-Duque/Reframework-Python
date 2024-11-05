import logging
from typing import Dict, Any, Union, List

from Framework.DatabaseConnection import DatabaseConnection


class Query(DatabaseConnection):
    def __init__(self, config: Dict[str, Any], logger: logging.Logger):
        super().__init__(config, logger)

    def encherFila(self, query: str) -> Union[List[tuple], None]:
        # Executa a query e retorna os resultados, garantindo que a conexão seja fechada corretamente.
        # query (str): A query SQL a ser executada.
        # Union[List[tuple], None]: Retorna a lista de resultados ou None em caso de erro.

        # Usando o bloco 'with' para garantir a abertura e fechamento da conexão
        with self as conn:
            results = conn.execute_query(query)
            if results:
                return results
            else:
                return None

