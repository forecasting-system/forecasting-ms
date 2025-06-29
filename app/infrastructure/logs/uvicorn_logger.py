import logging


class UvicornLogger():
    def __init__(self):
        self._logger = logging.getLogger("uvicorn")

    def info(self, msg: str) -> None:
        self._logger.info(msg)

    def warning(self, msg: str) -> None:
        self._logger.warning(msg)

    def error(self, msg: str) -> None:
        self._logger.error(msg)
