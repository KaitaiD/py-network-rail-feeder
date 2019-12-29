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
