# Overview

This is a test repository to demonstrate the use of a custom logging handler in Python. The intended goal is to have a handler that stores our log outputs, which can be written to a file or database in bulk.

## Features

1. **Singleton Handler**: Ensures only one instance of the logging handler exists, which stores all log records.
2. **Custom Variables**: Allows setting custom variables for each log entry.
3. **JSON Configuration**: Loads logging configuration from a JSON file.

## Class Overview

### [`ListLogHandler`](https://github.com/ThomasHepworth/stateful-logger/blob/master/logger/custom_handler.py#L6)

`ListLogHandler` is a custom logging handler that extends `logging.Handler`. It ensures that only one instance of the handler is created (Singleton pattern) and stores all log records.

#### Initialisation

The handler can be initialized with custom variables:

- `airflow_stage`: The stage of the Airflow pipeline.
- `mojap_version`: The version of Mojap.
- `dag_timestamp`: The timestamp of the DAG run.
- `task_timestamp`: The timestamp of the task run.
- `table`: The table name.

#### Methods

- **`emit(record)`**: Processes and stores each log record.
- **`_parse_event(event: str) -> Event`**: Parses a log event string into an `Event` namedtuple.
- **`_log_event(event_type: str, event_message: str) -> dict`**: Creates a dictionary with log event details and custom variables.
- **`_reset()`**: Resets the log records.
- **`_get_custom_logs() -> list`**: Retrieves all stored log records.
- **`dataframe() -> pd.DataFrame`**: Returns the log records as a pandas DataFrame.

## Example Output

Running main yields the following log outputs:

```python
[INFO|2878338676|L18] 2024-05-16T20:56:40+0100: Logging is configured and ready to use.
[WARNING|2878338676|L19] 2024-05-16T20:56:40+0100: Test
[INFO|hello|L7] 2024-05-16T20:56:40+0100: Hello;;;World!
[INFO|world|L7] 2024-05-16T20:56:40+0100: Hello, World!
```

These are all logged within our singleton class and can be retrieved using the `dataframe()` method.
```python
Stored logs as a DataFrame:
                                event_type event_message airflow_stage  \
0  Logging is configured and ready to use.                  production
1                                     Test                  production
2                                    Hello        World!    production
3                            Hello, World!                  production

  mojap_version         dag_timestamp        task_timestamp          table
0         1.0.0  2024-01-01T00:00:00Z  2024-01-01T01:00:00Z  example_table
1         1.0.0  2024-01-01T00:00:00Z  2024-01-01T01:00:00Z  example_table
2         1.0.0  2024-01-01T00:00:00Z  2024-01-01T01:00:00Z  example_table
3         1.0.0  2024-01-01T00:00:00Z  2024-01-01T01:00:00Z  example_table
```

A custom logger can then be used on top of this infrastructure to allow for easier interfacing with this logging handler.
