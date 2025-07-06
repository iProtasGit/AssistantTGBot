import logging


class ErrorCriticalLogFilter(logging.Filter):
    def filter(self, record):
        return record.levelname in ('ERROR', 'CRITICAL')


class DebugInfoLogFilter(logging.Filter):
    def filter(self, record):
        return record.levelname in ('DEBUG', 'INFO')


class CriticalLogFilter(logging.Filter):
    def filter(self, record):
        return record.levelname == 'CRITICAL'