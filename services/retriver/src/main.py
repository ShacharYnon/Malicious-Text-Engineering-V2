from .connector import DatabaseConnection 
from .dal import DalMongo
import logging
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)


class manager:

    def test_connection(self):
        connection = DatabaseConnection()
        connection.connect()


    def test_dal(self):
        dal = DalMongo()
        docs = dal.get_oldest_documents(time_stamp="2020-03-16T13:43:43.000+00:00", limit=2)
        for doc in docs:
            print(doc)


        
if __name__ == "__main__":
    mgr = manager()
    mgr.test_dal()