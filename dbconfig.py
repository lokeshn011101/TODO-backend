import mysql.connector as mysql


class MySQLDatabase:
    def __init__(self):
        self.mydb = mysql.connect(user='uoepyus8kbgfjsbu', password='yfZh18m7INgjupjSioA3',
                                  database='blrnqpxk1qyh5kjvauti', host='blrnqpxk1qyh5kjvauti-mysql.services.clever-cloud.com')
        self.mydb.disconnect()

    def connectDB(self):
        self.mydb = mysql.connect(user='uoepyus8kbgfjsbu', password='yfZh18m7INgjupjSioA3',
                                  database='blrnqpxk1qyh5kjvauti', host='blrnqpxk1qyh5kjvauti-mysql.services.clever-cloud.com')
        x = self.mydb.is_connected()
        if x == True:
            print(' * Database connected! :)')

    def disconnectDB(self):
        self.mydb.close()

        x = self.mydb.is_connected()
        if x == False:
            print(' * Database disconnected! :(')
