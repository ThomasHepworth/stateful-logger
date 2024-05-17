import logging
from typing import Tuple


class ListLogHandler(logging.Handler):

    def __init__(
        self,
        airflow_stage: str,
        mojap_version: str,
        dag_timestamp: str,
        task_timestamp: str,
        table: str,
    ):
        super().__init__()
        self.airflow_stage = airflow_stage
        self.mojap_version = mojap_version
        self.dag_timestamp = dag_timestamp
        self.task_timestamp = task_timestamp
        self.table = table
        self.log_records = []

    def _parse_event(self, record: logging.LogRecord) -> Tuple[str, str]:
        """
        Parse the log record to extract event type and message.
        """
        event_type = getattr(record, "event_type", record.levelname)
        event_message = self.format(record)
        return event_type, event_message

    def _log_event(self, event_type: str, event_message: str) -> dict:
        return {
            "event_type": event_type,
            "event_message": event_message,
            "airflow_stage": self.airflow_stage,
            "mojap_version": self.mojap_version,
            "dag_timestamp": self.dag_timestamp,
            "task_timestamp": self.task_timestamp,
            "table": self.table,
        }

    def emit(self, record: logging.LogRecord) -> None:
        event_type, event_message = self._parse_event(record)
        log_entry = self._log_event(event_type, event_message)
        self.log_records.append(log_entry)

    def reset(self) -> None:
        self.log_records = []

    def dataframe(self):
        import pandas as pd

        return pd.DataFrame(self.log_records)
