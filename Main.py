from Framework.EndProcess import EndProcess
from Framework.Exceptions import BusinessException
from Framework.Init import Init
from Framework.InitAllApplications import InitAllApplications
from Framework.ProcessTransaction import ProcessTransaction
from Framework.Selenium import Selenium


def main():
    init = Init()

    config = init.get_config()
    logger = init.get_logger()

    driver = Selenium(logger, config["Settings"]["SeleniumBrowser"]).get_driver()

    process_transaction = ProcessTransaction(driver, logger)

    end_process = EndProcess(driver, logger)

    transactions = InitAllApplications(driver,logger,config).work()

    try:
        for transaction in transactions:
            process_transaction.execute(transaction)
    except BusinessException as e:
        logger.info(f"{e}")
    except Exception as e:
        logger.error(f"excessão de sistema: {e}")
    end_process.finalize()


if __name__ == "__main__":
    main()
