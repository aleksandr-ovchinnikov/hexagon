import logging

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

logger = logging.Logger("logger")
handler = logging.FileHandler("./logs/logger.log")
handler.setFormatter(formatter)
logger.addHandler(handler)
