# Overview

This is a test repository to demonstrate the use of a custom logging handler in Python. The intended goal is to have a handler that stores our log outputs, which can be written to a file or database in bulk.

This sketch includes:
* A [custom handler](https://github.com/ThomasHepworth/stateful-logger/blob/master/logger/custom_handler.py), which tracks all log calls made in the system and writes this to a dictionary, as we are doing currently in [`append_log_data`](https://github.com/moj-analytical-services/airflow-hmcts-sdp-load/blob/main/load/load_logger.py#L120).
* A [custom logger](https://github.com/ThomasHepworth/stateful-logger/blob/master/logger/custom_logger.py) for interfacing with the handler
* A [setup step](https://github.com/ThomasHepworth/stateful-logger/blob/3b782bd634f81b10ef8c1bbaf5cd64610ec06db1/logger/setup_logger.py#L7) to ensure that our custom logger is set as the main logger to be imported and used and that the custom handler is added to all logging objects (it lives on the root).

Using the above allows us to load our custom handler at startup and track logs wherever a `logger.info` call is made.

Additionally, when a logger is setup using the common `getLogger` pattern, a `CustomLogger` class will be created.
```py
import logging

# Logger will be of class <CustomLogger>
logger = logging.getLogger(__name__)

# This will log to sysout and also be stored in a `log_records` attribute on the custom handler.
logger.info("My message")
```

## Diagrammatic Overview

Visually, the logging setup in this repo looks like so:

<p align="center">
  <img src="https://github.com/ThomasHepworth/stateful-logger/assets/45356472/d3e45931-7334-4e2c-ad60-c79086f39f10" width="60%" />
</p>

Here, handlers are attached to the root logger. These get passed to all child loggers (including our custom logger). 

Crucially, the `CustomLogger` can be set as our main logger with `logging.setLoggerClass`. When the `logging` module is called with `getLogger` going forward, the `CustomLogger` will be returned.

<hr>

## Class Overview

### [`ListLogHandler`](https://github.com/ThomasHepworth/stateful-logger/blob/master/logger/custom_handler.py#L6)

`ListLogHandler` is a custom logging handler that extends `logging.Handler`. It ensures that only one instance of the handler is created (Singleton pattern) and stores all log records.

#### Initialisation

The handler can be initialised with custom variables:

- `airflow_stage`: The stage of the Airflow pipeline.
- `mojap_version`: The version of Mojap.
- `dag_timestamp`: The timestamp of the DAG run.
- `task_timestamp`: The timestamp of the task run.
- `table`: The table name.

These can be set directly in the json configuration file or injected in on read.

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
  event_type                            event_message airflow_stage  \
0      setup  Logging is configured and ready to use.    production
1       test                                     Test    production
2        Big                                  Alert!!    production
3       INFO                           Hello;;;World!    production
4       INFO                            Hello, World!    production

  mojap_version         dag_timestamp        task_timestamp          table
0         1.0.0  2024-01-01T00:00:00Z  2024-01-01T01:00:00Z  example_table
1         1.0.0  2024-01-01T00:00:00Z  2024-01-01T01:00:00Z  example_table
2         1.0.0  2024-01-01T00:00:00Z  2024-01-01T01:00:00Z  example_table
3         1.0.0  2024-01-01T00:00:00Z  2024-01-01T01:00:00Z  example_table
4         1.0.0  2024-01-01T00:00:00Z  2024-01-01T01:00:00Z  example_table
```

A custom logger can then be used on top of this infrastructure to allow for easier interfacing with this logging handler.
