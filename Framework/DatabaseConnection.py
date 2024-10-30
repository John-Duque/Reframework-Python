import logging
from typing import Optional, Any, Union, Dict
import cx_Oracle
import mysql.connector
import pyodbc


class DatabaseConnection:
    # Classe responsável por gerenciar a conexão com o banco de dados.
    # Permite conexão via parâmetros individuais ou connection string.

    # Tipos utilizados dentro da classe
    DbConnectionType = Optional[
        Union[mysql.connector.MySQLConnection, pyodbc.Connection, cx_Oracle.Connection]
    ]
    ConfigType = Dict[str, Any]

    # Declaração dos atributos da classe
    db_type: str  # Tipo do banco de dados (mysql, sqlserver, oracle).
    host: str  # Endereço do servidor.
    database: str  # Nome do banco de dados.
    user: str  # Usuário de conexão.
    password: str  # Senha do usuário.
    port: Optional[int]  # Porta do banco de dados.
    pool_size: int  # Tamanho do pool de conexão.
    connection: DbConnectionType  # Conexão com o banco.
    logger: logging.Logger  # Logger para monitoramento.
    config: Dict[str, Any]

    def __init__(self, config: Dict[str, Any], logger: logging.Logger) -> None:

        # Inicializa a conexão com o banco de dados.

        self.connection: DatabaseConnection.DbConnectionType = None
        self.logger = logger
        self.config = config

        # Configura a conexão baseada na connection string ou nos parâmetros individuais
        self._configure_connection(
            self.config["Settings"]["Database"]["Parameters"]["Type"],
            self.config["Settings"]["Database"]["Parameters"]["Host"],
            self.config["Settings"]["Database"]["Parameters"]["Database"],
            self.config["Settings"]["Database"]["Parameters"]["User"],
            self.config["Settings"]["Database"]["Parameters"]["Password"],
            self.config["Settings"]["Database"]["Parameters"]["Port"],
            self.config["Settings"]["Database"]["Parameters"]["PoolSize"],
            self.config["Settings"]["Database"]["ConnectionString"]
        )

    def _configure_connection(
            self,
            db_type: Optional[str] = None,
            host: Optional[str] = None,
            database: Optional[str] = None,
            user: Optional[str] = None,
            password: Optional[str] = None,
            port: Optional[int] = None,
            pool_size: int = 5,
            connection_string: Optional[str] = None
    ) -> None:
        # Configura a conexão com base nos parâmetros ou na connection string.
        if connection_string:
            self._parse_connection_string(connection_string)
            self.pool_size = pool_size
        else:
            # Configuração manual via parâmetros individuais
            self.db_type = db_type.lower()
            self.host = host
            self.database = database
            self.user = user
            self.password = password
            self.port = port
            self.pool_size = pool_size

    def _parse_connection_string(self, connection_string: str) -> None:
        # Analisa a connection string e configura os atributos.
        try:
            if connection_string.startswith("mysql://"):
                self.logger.info("Usando conexão MySQL via connection string.")
                user_pass, host_db = connection_string.split("://")[1].split('@')
                user, password = user_pass.split(':')
                host, port_db = host_db.split(':')
                port, database = port_db.split('/')

                self.db_type = "mysql"
                self.host = host
                self.database = database
                self.user = user
                self.password = password
                self.port = int(port)

            elif connection_string.startswith("mssql+pyodbc://"):
                self.logger.info("Usando conexão SQL Server via connection string.")
                user_pass, host_db = connection_string.split('@')[0].split('//')[1], connection_string.split('@')[1]
                user, password = user_pass.split(':')
                host, port_db = host_db.split(':')
                port, database = port_db.split('/')

                self.db_type = "sqlserver"
                self.host = host
                self.database = database
                self.user = user
                self.password = password
                self.port = int(port)

            elif connection_string.startswith("oracle://"):
                self.logger.info("Usando conexão Oracle via connection string.")
                user_pass, host_db = connection_string.split("://")[1].split('@')
                user, password = user_pass.split(':')
                host, port_sid = host_db.split(':')
                port, sid = port_sid.split('/')

                self.db_type = "oracle"
                self.host = host
                self.database = sid
                self.user = user
                self.password = password
                self.port = int(port)

            else:
                raise ValueError(f"Tipo de connection string não suportado: {connection_string}")

        except Exception as e:
            self.logger.error(f"Erro ao analisar a connection string: {str(e)}")
            raise

    def __enter__(self) -> "DatabaseConnection":
        # Abre a conexão ao entrar no contexto.
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        # Fecha a conexão ao sair do contexto.
        self.close()

    def connect(self) -> None:
        # Estabelece a conexão com o banco de dados.
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

        except (mysql.connector.Error, pyodbc.Error, cx_Oracle.Error) as e:
            self.logger.error(f"Erro ao conectar ao banco de dados: {str(e)}")
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
