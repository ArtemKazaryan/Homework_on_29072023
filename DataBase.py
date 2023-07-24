import sqlite3


class DataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def get_menu(self):
        try:
            self.__cur.execute('SELECT * FROM menu')
            res = self.__cur.fetchall()
            if res:
                return res
        except IOError:
            print('Ошибка чтения данных')
        return []