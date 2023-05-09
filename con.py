import psycopg2 as pg


class Connection:
    

    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        return None

    def connect(self):
        try:
            connection = pg.connect(dbname=self.dbname, user=self.user, password=self.password, host=self.host, port=self.port)
            if connection:
                print("Connection to database successful!")

            return connection
        except Exception as e:
            print(e)
            return None

    def insert(self, query):
        try:
            connection = pg.connect(dbname=self.dbname, user=self.user, password=self.password, host=self.host, port=self.port)
            if connection:
                print("Connection to database successful!")
                #get cursor
                cursor = connection.cursor()
                #execute query
                cursor.execute(query)
                #commit changes
                connection.commit()
                #close cursor
                cursor.close()
                #close connection
                connection.close()
                #fetch data
                record = cursor.fetchall()
            return connection
        except Exception as e:
            print(e)
            return None
    def select(self, query, id):
        try:
            connection = pg.connect(dbname=self.dbname, user=self.user, password=self.password, host=self.host, port=self.port)
            if connection:
                print("Connection to database successful!")
                #get cursor
                cursor = connection.cursor()
                #execute query
                cursor.execute(query, (id,))
                #commit changes
                connection.commit()
                #fetch data
                record = cursor.fetchall()
            return record
        except Exception as e:
            print(e)
            return None

connections = Connection("face_recon", "mav", "21void", "localhost", "5432")
conn = connections.connect()