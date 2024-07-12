import logging
import datetime

LOG_FILE = "logs\logs_{}.txt".format(datetime.date.today())

logging.basicConfig(filename=LOG_FILE,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def send_message_error(message: str = '') -> None:
    """Envia uma mensagem de erro no arquivo log

    :param message: Mensagem. Padrão = ''
    """
    print(message)
    logger.error(message)


def send_message_info(message: str = '') -> None:
    """Envia uma mensagem informativo no arquivo log

    :param message: Mensagem. Padrão = ''
    """
    print(message)
    logger.info(message)