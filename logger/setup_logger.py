import logging
import json
import pathlib
from logger.custom_logger import CustomLogger


def setup_logging(
    airflow_stage: str,
    mojap_version: str,
    dag_timestamp: str,
    task_timestamp: str,
    table: str,
):
    """
    Setup logging configuration from a JSON file and initialize custom handler with given parameters.
    """
    logging.setLoggerClass(CustomLogger)
    config_file = pathlib.Path("logger/config.json")
    if config_file.exists():
        try:
            with open(config_file, "r") as f:
                config = json.load(f)

            # Check for listHandler in the configuration
            handler_config = config["handlers"].get("listHandler")
            if handler_config is None:
                raise ValueError(
                    "Handler 'listHandler' not found in configuration file."
                )

            # Set the handler variables
            handler_vars = {
                "airflow_stage": airflow_stage,
                "mojap_version": mojap_version,
                "dag_timestamp": dag_timestamp,
                "task_timestamp": task_timestamp,
                "table": table,
            }
            for key, value in handler_vars.items():
                handler_config[key] = value

            logging.config.dictConfig(config)
        except json.JSONDecodeError as e:
            raise ValueError(f"Error decoding JSON configuration file: {e}")
        except KeyError as e:
            raise ValueError(f"Configuration key error: {e}")
    else:
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
        logging.warning("Logging configuration file not found. Using default settings.")

    logger = logging.getLogger("pipeline_logger")
    return logger
