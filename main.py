import logging
from logger.setup_logger import setup_logging
from logger.custom_handler import ListLogHandler
from test_functions.hello import hello
from test_functions.world import world

if __name__ == "__main__":
    # Setup logging using the `CustomLogger` and input vars
    logger = setup_logging(
        airflow_stage="production",
        mojap_version="1.0.0",
        dag_timestamp="2024-01-01T00:00:00Z",
        task_timestamp="2024-01-01T01:00:00Z",
        table="example_table",
    )
    logger = logging.getLogger(__name__)

    logger.info("Logging is configured and ready to use.")
    logger.warning("Test")

    # Generate some logs from another module/script
    hello()
    world()

    # Get the stored logs -> these should include logs from this script and the imported modules
    print("\nStored logs as a DataFrame:")
    # Print the logs dataframe
    handler = next(
        (h for h in logger.parent.handlers if isinstance(h, ListLogHandler)), None
    )
    if handler:
        print(handler.dataframe())
