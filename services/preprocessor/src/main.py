from .. import config
import logging
from .data_processor import DataProcessor
from .consumer import Consumer
from .publisher import Publisher
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class ProcessManager:
    def __init__(self):
        self.publisher = Publisher()
        self.topic_anti = config.KAFKA_TOPIC_ANTI
        self.topic_not_anti = config.KAFKA_TOPIC_NOT_ANTI
        self.data = None
        self.processor = DataProcessor()