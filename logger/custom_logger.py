import logging
from logger.custom_handler import ListLogHandler
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from pandas import DataFrame


class CustomLogger(logging.Logger):
    # Class-level attributes for environment variables
    airflow_stage = ""
    mojap_version = ""
    dag_timestamp = ""
    task_timestamp = ""
    table = ""

    def __init__(self, name: str, level: int = logging.NOTSET):
        super().__init__(name, level)
        self._list_handler: Optional[ListLogHandler] = None

    @staticmethod
    def _find_handler(logger: logging.Logger, handler_type: logging.Handler):
        # Recursively search for a handler of a given type
        while logger:
            for handler in logger.handlers:
                if isinstance(handler, handler_type):
                    return handler
            logger = logger.parent

        raise ValueError(
            f"Handler of type {handler_type} not found in logger hierarchy."
        )

    @property
    def list_handler(self) -> ListLogHandler:
        if self._list_handler is None:
            self._list_handler = CustomLogger._find_handler(self, ListLogHandler)
        return self._list_handler

    @property
    def log_records(self):
        self.list_handler.log_records

    def dataframe(self) -> "DataFrame":
        return self.list_handler.dataframe()
