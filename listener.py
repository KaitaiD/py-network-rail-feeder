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
        
        
class BaseListener(object):
    """
    Make a Base Listener. This can facilitate to create different listeners for different feeds.
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
        pass

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

    def _flatten(self, d, parent_key='', sep='_'):
        """
        An function to flatten the nested dictionary and connect the different levels
        of dictionaries with _ symbol
        """
        items = []
        for k, v in d.items():
            new_key = parent_key + sep + k if parent_key else k
            try:
                items.extend(self._flatten(v, new_key, sep=sep).items())
            except:
                items.append((new_key, v))
        return dict(items)


class MVListener(BaseListener):
    """
    Make a Listener for Train Movement Feeds.
    """
    def __init__(self, messager, view=False):
        """
        Args:
            messager: MessagerToSQL object
            view: If True, will print all message instead of saving. Default is False
        """
        self.view = view
        super().__init__(messager)

    def on_message(self, headers, messages):
        logger.info(headers)
        for message in json.loads(messages):
            if view:
                print(message['body'])
            else:
                self._insert_message(message['body'])
                
class PPMListener(BaseListener):
    """
    Make a Listener for Public Performance Measures (PPM) Feeds.
    """
    def __init__(self, messager, view=False):
        """
        Args:
            messager: MessagerToSQL object
            view: If True, will print all message instead of saving. Default is False
        """
        self.view = view
        super().__init__(messager)

    def on_message(self, headers, messages):
        logger.info(headers)
        data = json.loads(messages)
        for message in data["RTPPMDataMsgV1"]['RTPPMData']['OperatorPage']:
            if self.view:
                print(self.flatten(message['Operator']))
            else:
                self._insert_message(self.flatten(message['Operator']))

class VSTPListener(BaseListener):
    """
    Make a Listener for VSTP (Very Short Term Planning) Feeds.
    """
    def __init__(self, messager, view=False):
        """
        Args:
            messager: MessagerToSQL object
            view: If True, will print all message instead of saving. Default is False
        """
        self.view = view
        super().__init__(messager)

    def on_message(self, headers, messages):
        logger.info(headers)
        data = json.loads(messages)
        if self.view:
            print(data['VSTPCIFMsgV1']['schedule'])
        else:
            self._insert_message(data['VSTPCIFMsgV1']['schedule'])

 class TDListener(BaseListener):
    """
    Make a Listener for train describer (TD) Feeds.
    """
    def __init__(self, messager, view=False):
        """
        Args:
            messager: MessagerToSQL object
            view: If True, will print all message instead of saving. Default is False
        """
        self.view = view
        super().__init__(messager)

    def on_message(self, headers, messages):
        logger.info(headers)
        data = json.loads(messages)
        new_key = "MSG"
        for message in data:
            for k, v in message.items():  
                new_formed_message = {**{new_key: k}, **v}
                if self.view:
                    print(new_formed_message)
                else:
                    self._insert_message(new_formed_message)
