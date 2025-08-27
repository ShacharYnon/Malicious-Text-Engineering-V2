from .connector import DatabaseConnection 



class manager:

    def test_connection(self):
        connection = DatabaseConnection()
        connection.connect()


        
if __name__ == "__main__":
    m = manager()
    print(m.test_connection())
    