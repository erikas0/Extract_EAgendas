import logging

from config.properties import SOLUCAO

# Configuração do logger
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(
    level=logging.DEBUG,
    format=LOG_FORMAT,
    datefmt=DATE_FORMAT,
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
)


logger = logging.getLogger(SOLUCAO)
