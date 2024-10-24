from Framework.GetTransaction import GetTransaction
from Framework.Selenium import Selenium
from Framework.ProcessTransaction import ProcessTransaction
from Framework.EndProcess import EndProcess
from Framework.Init import Init
from Framework.Exceptions import BusinessException, ApplicationException


def main():
    init = Init()

    selenium = Selenium(init.get_logger(), init.get_config()["Settings"]["SeleniumBrowser"])

    transactions = [
        {"id": 1, "amount": 100, "description": "Selenium Python"},
        {"id": 2, "amount": -50, "description": "Teste com valor negativo"}
    ]

    get_transaction = GetTransaction(transactions)

    process_transaction = ProcessTransaction(selenium.get_driver(), init.get_logger())

    end_process = EndProcess(selenium.get_driver(), init.get_logger())

    process_transaction.execute(get_transaction.get_all())

    end_process.finalize()


if __name__ == "__main__":
    main()
