from configparser import ConfigParser
from psycopg2 import (
    connect,
    DatabaseError,
)


class WorkerSQL:

    def __init__(self, get_settings, settings, section):

        self.get_settings = get_settings
        self.filename = settings
        self.section = section

        self.parser = ConfigParser()
        self.database = dict()
        self.data = dict()

        self.connection = None

    # Прямое подключение к PostgreSQL.
    def connectPostgreSQL(self):
        try:
            self.connection = connect(**self.databaseCheck(), connect_timeout=4)

            cursor = self.connection.cursor()
            cursor.execute(self.get_settings)

            self.data = cursor.fetchall()

            cursor.close()

            return self.data

        except (Exception, DatabaseError) as ex:
            print(f"[!] [SQL] Error on connectPostgreSQL func >> connection to server, more info : {ex}")

        finally:
            if self.connection is not None:
                self.connection.close()

                # print('\n[+] [SQL] Request : [{0}] completed, connection closed'.format(self.get_settings))

                print('\n[+] [SQL] Request : [{0}] completed, connection closed'.format(self.get_settings))
            else:
                pass

    # Insert для PostgrSQL
    def addPostgreSQL(self):
        try:
            self.connection = connect(**self.databaseCheck(), connect_timeout=8)

            cursor = self.connection.cursor()
            cursor.execute(self.get_settings)

            cursor.close()

            print("[+] [SQL] Insert : [{0}] completed, connection closed".format(self.get_settings))

        except Exception as ex:
            print(ex)

    # Подключение к PostgreSQL с перебором всех столбцов дат.
    def editTableWithoutThreads(self, callback_data):
        try:
            self.connection = connect(**self.databaseCheck())

            cursor = self.connection.cursor()
            for time in callback_data:
                cursor.execute("{0} WHERE crnt_date = '{1}'".format(self.get_settings, time[8]))

            self.connection.commit()

        except (Exception, DatabaseError) as ex:
            print("[!] [SQL] Error on editTableWithoutThreads func >> connection to server, more info : {0}".format(ex))

        finally:
            if self.connection is not None:
                self.connection.close()

                print('\n[+] [SQL] Request : [{0}] completed, connection closed'.format(self.get_settings))

    # Подключение к PostgreSQL с изменением столбцов по id.
    def editGovWithoutThreads(self, callback_data):
        try:
            self.connection = connect(**self.databaseCheck())

            cursor = self.connection.cursor()
            for id_row in callback_data:
                cursor.execute("{0} WHERE id = '{1}'".format(self.get_settings, id_row))

            self.connection.commit()

        except (Exception, DatabaseError) as ex:
            print("[!] [SQL] Error on editGovWithoutThreads func >> connection to server, more info : {0}".format(ex))

        finally:
            if self.connection is not None:
                self.connection.close()

                print('\n[+] [SQL] Request : [{0}] completed, connection closed'.format(self.get_settings))

    # Проверка файла перед соединением.
    def databaseCheck(self):
        self.parser.read(self.filename)

        if self.parser.has_section(self.section):
            params = self.parser.items(self.section)
            for param in params:
                self.database[param[0]] = param[1]
        else:
            raise Exception('\n[-] File "{0}" not found on "{1}" folder'.format(self.section, self.filename))

        return self.database


class AddHosts:
    def __init__(self):
        self.message = 'нет подключения'
        self.settings = 'settings/database.ini'
        self.section = 'postgresql'

    def infoPostgreSQL(self):
        currentDateServer = str(self.requestPostgreSQL("SELECT version(), CURRENT_DATE;")[0])
        print("Current info from server: {0}".format(currentDateServer))

    def appendHostPostgreSQL(self, db, host, port, username, password, dirs, files):
        self.addPostgreSQL("INSERT INTO public.\"{0}\" (ip_address, port_opened, user_name, pass, dirs, files) "
                           "VALUES ('{1}', '{2}', '{3}', '{4}', '{5}', '{6}'); commit;"
                           .format(db, host, port, username, password, dirs, files))

    def requestPostgreSQL(self, request):
        return WorkerSQL(request, self.settings, self.section).connectPostgreSQL()

    def addPostgreSQL(self, request):
        return WorkerSQL(request, self.settings, self.section).addPostgreSQL()
