from logging import FileHandler
from backend.modules import logging, LOGGING_PATH, os

__all__ = ["Log"]


class Logging:
    def __init__(self, filename="app.log", level=logging.INFO):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level)
        if not self.logger.handlers:
            logDir = LOGGING_PATH
            logFileDir = os.path.join(logDir, filename)
            os.makedirs(logDir, exist_ok=True)
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            fileHandler = logging.FileHandler(logFileDir)
            fileHandler.setFormatter(formatter)
            fileHandler.setLevel(level)

            # Stream Handler (for console output)
            streamHander = logging.StreamHandler()
            streamHander.setFormatter(formatter)
            streamHander.setLevel(level)

            self.logger.addHandler(fileHandler)
            self.logger.addHandler(streamHander)

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

    def debug(self, message):
        self.logger.debug(message)

    def critical(self, message):
        self.logger.critical(message)

    def warning(self, message):
        self.logger.warning(message)


Log = Logging()
