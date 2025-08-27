from .connector import DatabaseConnection 
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


        
if __name__ == "__main__":
    m = manager()
    m.test_connection()
    