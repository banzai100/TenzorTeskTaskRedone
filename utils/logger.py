from loguru import logger

logger.add("logs/test_logs.log", format="{time:YYYY-MM-DD HH:mm:ss} {level} {message}", level="INFO")


def log_info(message):
    logger.info(message)


def log_error(message):
    logger.error(message)
