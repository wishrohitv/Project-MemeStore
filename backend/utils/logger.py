from backend.modules import LOGGING_PATH, logging, os

__all__ = ["Log", "Logging"]


class Logging:
    def __init__(self, name, filename="app.log", level=logging.INFO):

        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        # self.logger.propagate = False

        logDir = LOGGING_PATH
        os.makedirs(logDir, exist_ok=True)

        logFile = os.path.join(logDir, filename)

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        fileHandler = logging.FileHandler(logFile)
        fileHandler.setLevel(level)
        fileHandler.setFormatter(formatter)

        streamHandler = logging.StreamHandler()
        streamHandler.setLevel(level)
        streamHandler.setFormatter(formatter)

        self.logger.addHandler(fileHandler)
        self.logger.addHandler(streamHandler)

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


Log = Logging(__name__)
