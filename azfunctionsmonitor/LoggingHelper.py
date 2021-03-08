import logging
import os
from typing import Any, Dict, MutableMapping, Optional

import azure.functions as func
from opencensus.ext.azure.log_exporter import AzureLogHandler


class LoggingHelper:
    def __init__(self, prefix: str, logger: logging.Logger):
        # super(LoggingHelper, self).__init__(logger, {})
        self.adapter = logging.LoggerAdapter(logger, {})
        self.prefix = prefix

    def process(self, msg: str, kwargs: MutableMapping[str, Any]):
        return "[%s] %s" % (self.prefix, msg), kwargs

    def debug(self, msg: str, context: Optional[func.Context] = None, correlation_id: Optional[str] = None, record: Optional[Dict[str, str]] = None) -> None:
        extra = self._get_properties(context, correlation_id, record)
        return self.adapter.debug(msg, extra=extra)

    def info(self, msg: str, context: Optional[func.Context] = None, correlation_id: Optional[str] = None, record: Optional[Dict[str, str]] = None) -> None:
        extra = self._get_properties(context, correlation_id, record)
        return self.adapter.info(msg, extra=extra)

    def warning(self, msg: str, context: Optional[func.Context] = None, correlation_id: Optional[str] = None, record: Optional[Dict[str, str]] = None) -> None:
        extra = self._get_properties(context, correlation_id, record)
        return self.adapter.warning(msg, extra=extra)

    def error(self, msg: str, context: Optional[func.Context] = None, correlation_id: Optional[str] = None, record: Optional[Dict[str, str]] = None) -> None:
        extra = self._get_properties(context, correlation_id, record)
        return self.adapter.error(msg, extra=extra)

    def exception(
        self, msg: str, context: Optional[func.Context] = None, correlation_id: Optional[str] = None, record: Optional[Dict[str, str]] = None
    ) -> None:
        extra = self._get_properties(context, correlation_id, record)
        return self.adapter.exception(msg, extra=extra)

    def _get_properties(self, context: Optional[func.Context], correlation_id: Optional[str], record: Optional[Dict[str, str]]):
        properties = {
            "custom_dimensions": {
                "CorrelationId": correlation_id if correlation_id is not None else "-- not provided --",
                "invocationid": context.invocation_id if context is not None else "-- no context --",
            }
        }

        # pyright: reportUnnecessaryIsInstance=false
        if record is not None and isinstance(record, dict):
            properties["custom_dimensions"].update(record)

        return properties


def get_logger(prefix: str, name: Optional[str] = None) -> LoggingHelper:
    LOGLEVEL = os.environ.get("LOGLEVEL", "WARNING").upper()
    logging.basicConfig(level=LOGLEVEL)

    if name is not None:
        logger = logging.getLogger(name=name)
    else:
        logger = logging.getLogger()

    try:
        azure_handler = AzureLogHandler()
        logger.addHandler(azure_handler)
    except ValueError as e:
        logger.exception(f"failed to load opencensus AzureLogHandler: {e}", exc_info=e)

    except Exception as e:
        logger.exception(f"failed to load opencensus AzureLogHandler another reason: {e}", exc_info=e)

    logger.setLevel(level=LOGLEVEL)

    log_adapter = LoggingHelper(prefix, logger)
    log_adapter.warning(f"logging set to {LOGLEVEL}")
    return log_adapter
