from .dal import DalMongo
import logging
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)
import time
import datetime
from .. import config
from .publisher import Publisher



class manager:

    def __init__(self):
        self.dal = DalMongo()
        self.publisher = Publisher()
        self.topic_anti = config.KAFKA_TOPIC_ANTI
        self.topic_not_anti = config.KAFKA_TOPIC_NOT_ANTI
        self.data = None




    def main(self):
        self.data = self.dal.get_oldest_documents()
        while True:
            for docs in self.data:
                anti = []
                not_anti = []
                for doc in docs:
                    if doc.get("Antisemitic", False):
                        anti.append(doc)
                    else:
                        not_anti.append(doc)
                if anti:
                    self.publisher.publish(self.topic_anti, anti)
                if not_anti:
                    self.publisher.publish(self.topic_not_anti, not_anti)
                logging.info(f"Published {len(anti)} antisemitic and {len(not_anti)} non-antisemitic documents")
                print("waiting for 60 seconds")
                time.sleep(10)



            
if __name__ == "__main__":
    mgr = manager()
    # mgr.test_dal()
    mgr.main()
    