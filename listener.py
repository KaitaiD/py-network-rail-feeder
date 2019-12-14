import logging
import json

import sqlite3

logger = logging.getLogger("Listener Logger")

class MessagerToSQL(object):
    """
    Convert the messages received from feeds into sqlite database
    """
    def __init__(self, 
                 fp: str, 
                 schema: dict, 
                 drop_if_exists=True):
        """
        fp: Database name
        schema: Schema of the fields to collect from data feeds
        drop_if_exists: If true, drop the table if it exists already to avoid raising a sqlite error.
        """
        self.table_name = fp.split(".")[0]
        self.schema = schema
        
        # Reconstruct schema to be accepted by sqlite3
        self.printable_schema = ", ".join([" ".join([k, v]) for k,v in schema.items()])
        self.conn = sqlite3.connect(fp, check_same_thread=False)

        self.c = self.conn.cursor()
        if drop_if_exists:
            self.c.execute(f"DROP TABLE IF EXISTS {self.table_name}")
        self.c.execute(f"CREATE TABLE {self.table_name} ({self.printable_schema})")

    def insert(self, sql: str, msg_list: list):
        """
        Make a simple Python wrapper of insert method in sqlite.
        
        Args:
            sql: A SQL string of command
            msg_list: The list containing values of fields that need to be saved in sql table
        """
        self.c.execute(sql, msg_list)
        self.conn.commit()

    def close(self):
        """
        Make a simple Python wrapper to close connection to sql table
        """
        self.conn.close()
        

class MVListener(object):
    """
    Make a Listener for Train Movement Feeds.
    """
    def __init__(self, messager):
        """
        Args:
            messager: MessagerToSQL object
        """
        self.msger = messager

    def on_error(self, headers, message):
        logger.error(f"ERROR: {headers} {message}")

    def on_message(self, headers, messages):
        logger.info(headers)
        for message in json.loads(messages):
            self._insert_message(message['body'])

    def _insert_message(self, msg: str):
        """
        An internal function to insert the message to sql table.
        
        Args:
            msg: Customized message for MV
        """
        columns = self.msger.schema.keys()
        placeholders = ", ".join("?" * len(columns))

        sql = f"INSERT INTO {self.msger.table_name} VALUES ({placeholders})"
        self.msger.insert(sql, [msg.get(col) for col in columns])
