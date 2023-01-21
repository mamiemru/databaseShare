import os
import sqlite3

from sqlite3 import Error

FOLDER_BASE_PATH = os.getcwd()

class SqliteInterface:

    db = None

    def filepath(self, suffix):
        return f"{FOLDER_BASE_PATH}/{suffix}"

    def populate(self, db_schema="./schema.sql"):
        if not self.db:
            self.connect()

        with open(self.filepath(db_schema), 'r') as file:
            for line in file.read().split('\n\n'):
                self.db.execute(line)
        
        self.disconnect()

    def connect(self, db_file="./db.sqlite"):
        if not self.db:
            try:
                self.db = sqlite3.connect(self.filepath(db_file))
            except Error as e:
                raise e
        return self.db

    def disconnect(self):
        if self.db:
            self.db.close()
            self.db = None

    def beginTransaction(self):
        if not self.db:
            self.connect()
        cur = self.db.cursor()
        cur.execute("BEGIN")
        return cur

    def rollback(self, cur):
        cur.execute("ROLLBACK")

    def commit(self, cur):
        cur.execute("COMMIT")

