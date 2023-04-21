import logging

import json_log_formatter


class DjangoJSONFormatter(json_log_formatter.JSONFormatter):

    def json_record(self, message: str, extra: dict, record: logging.LogRecord) -> dict:
        """
        add custom list of keys to logs
        key request is removed because some django loggers try to pass the entire HttpRequest object
        which is not serializable as JSON by the library
        """
        if "request" in extra:
            extra.pop("request")
        extra.update({
            'funcName': record.funcName,
            'levelname': record.levelname,
            'module': record.module,
        })
        return super().json_record(message, extra, record)
