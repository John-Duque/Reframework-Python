import logging
from typing import Optional, Any, Union, Dict

import cx_Oracle
import mysql.connector
import pyodbc


class DatabaseConnection:
    db_type: str  # Tipo do banco de dados (mysql, sqlserver, oracle).
    host: str  # Endereço do servidor.
    database: str  # Nome do banco de dados.
    user: str  # Usuário de conexão.
    password: str  # Senha do usuário.
    port: Optional[int]  # Porta do banco (padrão depende do tipo).
    pool_size: int  # Tamanho do pool de conexão.
    connection: Optional[Union[mysql.connector.MySQLConnection, pyodbc.Connection, cx_Oracle.Connection]]
    logger: logging.Logger

    def __init__(self, logger: logging.Logger, db_type: str, host: str, database: str, user: str, password: str,
                 port: Optional[int] = None,
                 pool_size: int = 5) -> None:
        # Inicializa a classe de conexão com parâmetros específicos.
        self.db_type = db_type.lower()
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.pool_size = pool_size
        self.connection = None
        self.logger = logger

    def __enter__(self) -> Any:
        # Abre a conexão ao entrar no contexto.
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        # Fecha a conexão ao sair do contexto.
        self.close()

    def connect(self) -> None:
        """Estabelece a conexão com o banco de dados."""
        try:
            match self.db_type:
                case "mysql":
                    self.connection = mysql.connector.connect(
                        pool_name="mypool",
                        pool_size=self.pool_size,
                        host=self.host,
                        user=self.user,
                        password=self.password,
                        database=self.database,
                        port=self.port or 3306
                    )
                    self.logger.info("Conectado ao MySQL com sucesso.")

                case "sqlserver":
                    connection_string = (
                        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                        f"SERVER={self.host},{self.port or 1433};"
                        f"DATABASE={self.database};"
                        f"UID={self.user};PWD={self.password}"
                    )
                    self.connection = pyodbc.connect(connection_string)
                    self.logger.info("Conectado ao SQL Server com sucesso.")

                case "oracle":
                    dsn = cx_Oracle.makedsn(self.host, self.port or 1521, sid=self.database)
                    self.connection = cx_Oracle.connect(self.user, self.password, dsn)
                    self.logger.info("Conectado ao Oracle com sucesso.")

                case _:
                    raise ValueError(f"Banco de dados '{self.db_type}' não é suportado.")

        except mysql.connector.Error as e:
            self.logger.error(f"Erro ao conectar ao MySQL: {str(e)}")
            raise
        except pyodbc.Error as e:
            self.logger.error(f"Erro ao conectar ao SQL Server: {str(e)}")
            raise
        except cx_Oracle.Error as e:
            self.logger.error(f"Erro ao conectar ao Oracle: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Erro inesperado: {str(e)}")
            raise

    def execute_query(self, query: str) -> Union[list, None]:
        # Executa uma query no banco de dados.
        if not self.connection:
            self.logger.error("Conexão não estabelecida.")
            return None

        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            self.logger.info(f"Query executada com sucesso: {query}")
            return results
        except Exception as e:
            self.logger.error(f"Erro ao executar a query: {str(e)}")
            raise
        finally:
            cursor.close()

    def execute_procedure(self, procedure_name: str, params: Optional[Dict[str, Any]] = None) -> None:
        # Executa uma procedure armazenada no banco de dados.
        # procedure_name (str): Nome da procedure a ser executada.
        # params (Optional[Dict[str, Any]]): Parâmetros para a procedure.

        if not self.connection:
            self.logger.error("Conexão não estabelecida.")
            return

        try:
            cursor = self.connection.cursor()

            if self.db_type == "mysql" or self.db_type == "sqlserver":
                if params:
                    cursor.callproc(procedure_name, list(params.values()))
                else:
                    cursor.callproc(procedure_name)

            elif self.db_type == "oracle":
                param_list = [cx_Oracle.Parameter(name, value) for name, value in (params or {}).items()]
                cursor.callproc(procedure_name, param_list)

            self.logger.info(f"Procedure '{procedure_name}' executada com sucesso.")
        except Exception as e:
            self.logger.error(f"Erro ao executar a procedure '{procedure_name}': {str(e)}")
            raise
        finally:
            cursor.close()

    def close(self) -> None:
        # Fecha a conexão com o banco de dados.
        if self.connection:
            self.connection.close()
            self.logger.info("Conexão fechada com sucesso.")
        else:
            self.logger.warning("Nenhuma conexão ativa para fechar.")
