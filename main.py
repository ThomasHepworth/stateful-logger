from logger.setup_logger import setup_logging
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

    logger.info(
        "Logging is configured and ready to use.", extra={"event_type": "setup"}
    )
    logger.warning("Test", extra={"event_type": "test"})
    logger.error("Alert!!", extra={"event_type": "Big"})

    # Generate some logs from another module/script
    hello()
    world()

    # Get the stored logs -> these should include logs from this script and the imported modules
    print("\nStored logs as a DataFrame:")
    # Print the logs dataframe
    print(logger.dataframe())
