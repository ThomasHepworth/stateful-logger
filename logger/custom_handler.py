import logging
from collections import namedtuple
from typing import Optional


class ListLogHandler(logging.Handler):
    _instance: Optional["ListLogHandler"] = None
    event_delimiter = ";;;"
    Event = namedtuple("Event", ["event_type", "event_message"])

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
        self, airflow_stage, mojap_version, dag_timestamp, task_timestamp, table
    ):
        if not hasattr(self, "_initialized"):
            super().__init__()
            self._initialized = True
            self.airflow_stage = airflow_stage
            self.mojap_version = mojap_version
            self.dag_timestamp = dag_timestamp
            self.task_timestamp = task_timestamp
            self.table = table
            self.log_records = []

    def _parse_event(self, event: str) -> Event:
        event_split = event.split(self.event_delimiter, maxsplit=2)
        if len(event_split) == 1:
            return self.Event(event_split[0], "")
        return self.Event(event_split[0], event_split[1])

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

    def emit(self, record):
        event = self._parse_event(self.format(record))
        log_entry = self._log_event(event.event_type, event.event_message)
        self.log_records.append(log_entry)

    def _reset(self):
        self.log_records = []

    def _get_custom_logs(self):
        return self.log_records

    def dataframe(self):
        import pandas as pd

        logs = self._get_custom_logs()
        return pd.DataFrame(logs)
