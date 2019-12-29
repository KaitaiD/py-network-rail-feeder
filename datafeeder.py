import os
import time
import logging

import stomp
import sqlite3
import pandas as pd

from listener import MVListener, MessagerToSQL

logger = logging.getLogger("DataFeeder Logger")

HOSTNAME = "datafeeds.networkrail.co.uk"
# This provide a static mapping between topic of feed and corresponding listener, right now only MVListener is implemented
TOPIC_LISTENER_MAPPING = {
    "MVT": MVListener,
    "PPM": PPMListener,
    'VSTP': VSTPListener
}


class RailDataFeeder:
    """RailDataFeeder is a Python API to collect and save the real-time data from UK Network Rail Data Feed."""
    def __init__(self, 
                 db_name: str, 
                 schema: dict, 
                 topic: str,
                 channel: str,
                 username: str = os.getenv("DATAFEED_USERNAME"), 
                 password: str = os.getenv("DATAFEED_PW"),
                 drop_if_exists: bool = True,
                 view: bool = False
                 ):
        """
        Args:
            db_name: Name of sqlite database
            schema: A dictionary containing the fields needed from the data feeds and corresponding data type
            topic: Topic of channel
            channel: Topic channel in data feed
            username: Registered username. Default is to obtain from your local environment variable
            password: Password to log in data feed. Default is to obtain from your local environment variable
            drop_if_exists: If True, will drop the table if it exists already before inserting data into it. If
                False and the same table already exists, it will raise an error. Default is True
            view: If True, will only print message instead of saving. Default is False
        """
        self.table_name = db_name.split(".")[0]
        self.db_name = db_name
        self.username = username
        self.password = password
        if topic not in TOPIC_LISTENER_MAPPING.keys():
            raise NotImplementedError(f"Only topics in {TOPIC_LISTENER_MAPPING.keys()} are implemented.")
        self.topic = topic
        self.listener = TOPIC_LISTENER_MAPPING[topic]
        self.channel = channel
        self.schema = schema
        self.view = view
        self.msger = MessagerToSQL(fp=db_name, schema=schema, drop_if_exists=drop_if_exists)

    def _connect_data_feed(self):
        """
        Internal function to connect data feed using stomp connection.
        """
        conn = stomp.Connection(host_and_ports=[(HOSTNAME, 61618)])
        conn.set_listener('listener', self.listener(self.msger, self.view))
        conn.start()
        conn.connect(username=self.username, passcode=self.password)

        conn.subscribe(destination=f"/topic/{self.channel}", id=1, ack='auto')
        return conn

    def download_feed(self):
        """
        Download the data and save the json data to local device.
        """
        conn = self._connect_data_feed()

        while True:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                logger.info("Quit saving data to table and disable the connection with data feed!")
                break

        self.msger.close()
        conn.disconnect()

    def to_pandas(self, db_name: str = None, table_name: str = None) -> pd.DataFrame:
        """
        Read the sqlite table into a pandas DataFrame.
        
        Args:
            db_name: Database name. If None, will use the one defined during initalization of datafeeder. Default is None
            table_name: Table name. If None, will use defined table name in datafeeder. Default is None
            
        Returns:
            df: pandas DataFrame
        """
        if db_name is None:
            db_name = self.db_name
            table_name = self.table_name
        conn = sqlite3.connect(db_name)
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        return df
