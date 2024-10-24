from typing import List


class GetTransaction:
    transactionData: List[object]

    def __init__(self, transactionData: List[object]) -> None:
        # Inicializa a classe com uma lista genérica de objetos.
        self.transactionData = transactionData

    def get_all(self) -> List[object]:
        # Retorna todos os objetos da lista.
        return self.transactionData
