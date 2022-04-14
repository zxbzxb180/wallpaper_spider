from loguru import logger

logger.add('logs/runtime_{time}.log', mode='w', enqueue=True, rotation='12:00', retention='10 days')

