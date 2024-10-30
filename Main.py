from Components.Query import Query
from Framework.EndProcess import EndProcess
from Framework.GetTransaction import GetTransaction
from Framework.Init import Init
from Framework.ProcessTransaction import ProcessTransaction
from Framework.Selenium import Selenium


def main():
    init = Init()

    config = init.get_config()
    logger = init.get_logger()

    selenium = Selenium(logger, config["Settings"]["SeleniumBrowser"])

    driver = selenium.get_driver()

    db = Query(config, logger)

    results = db.encherFila("SELECT * FROM credits")

    get_transaction = GetTransaction(results)

    process_transaction = ProcessTransaction(driver, logger)

    end_process = EndProcess(driver, logger)

    process_transaction.execute(get_transaction.get_all())

    end_process.finalize()


if __name__ == "__main__":
    main()
