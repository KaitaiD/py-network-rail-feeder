import os
import time
import logging

import stomp
import sqlite3
import pandas as pd

from listener import MVListener, PPMListener, VSTPListener, TDListener, MessagerToSQL
from topicmapping import topic_mapping

pd.options.display.max_columns = None

# four topics to choose from - 1. MVT 2. PPM 3. VSTP 4. TD
TOPIC = "MVT"

train_rdf = RailDataFeeder(
                    db_name=topic_mapping[TOPIC][2], 
                    channel=topic_mapping[TOPIC][1], 
                    topic=TOPIC,
                    schema=topic_mapping[TOPIC][0],
                    username=USERNAME,
                    password=PASSWORD,
                    drop_if_exists=True,
                    view=False
)

train_rdf.download_feed()
train_ppm_rdf.to_pandas()
