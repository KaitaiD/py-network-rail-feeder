# py-network-rail-feeder
Network Data Feed provides some real-time open data from the rail industry in Great Britain. And this is an Python implementation to collect and download data from UK Network Rail Data Feed.

## Data Source
This is the site where you register and log in to subscribe different data feeds:
https://datafeeds.networkrail.co.uk/ntrod/myFeeds

There is a wiki page where you could find some documentation about this data feed:
https://wiki.openraildata.com/index.php/Main_Page

## Install package dependencies
First of all, you need to install all dependencies required by this tool.

```bash
pip install -r requirements.txt
```

## Why use SQL

Since the output of feeds are mostly in JSON format, and it is quite different to constantly saving updated real-time JSON. Therefore, I choose to save it in to sqlite database. And before saving, you need to specify the data schema for creating SQL table. Another reason is there are many fields in the JSON format, and maybe not everything is useful, therefore, you could cherry-pick the fields you need to save.

To define schema, you could check the WIKI page and find the documentation.

## Current Implementations / How to use it?

Right now, I only implement for two fields: Train Movement and TD

For instance:

```python
# Train Movement data feeder

mv_schema = {
    "event_type": "TEXT", 
    "gbtt_timestamp": "TEXT",
    "original_loc_stanox": "TEXT",
    "planned_timestamp": "INTEGER",
    "timetable_variation": "TEXT",
    "current_train_id": "INTEGER",
    "next_report_run_time": "INTEGER",
    "reporting_stanox": "INTEGER",
    "actual_timestamp": "INTEGER",
    "correction_ind": "TEXT",
    "event_source": "TEXT",
    "platform": "TEXT",
    "division_code": "TEXT",
    "train_terminated": "TEXT",
    "train_id": "INTEGER",
    "variation_status": "TEXT",
    "train_service_code": "INTEGER",
    "toc_id": "INTEGER",
    "loc_stanox": "INTEGER",
    "auto_expected": "TEXT",
    "direction_ind": "TEXT",
    "route": "TEXT",
    "planned_event_type": "TEXT",
    "next_report_stanox": "INTEGER",
}

# you could also choose specific TOC, e.g. "TRAIN_MVT_TOC_HT" as topic
mv_channel = "TRAIN_MVT_ALL_TOC"

train_mv_rdf = RailDataFeeder(
                    db_name="train_mv_all_toc.db", 
                    channel=mv_channel, 
                    topic="MVT",
                    schema=mv_schema,
                    username=USERNAME,
                    password=PASSWORD,
                    drop_if_exists=True
)

train_mv_rdf.download_feed()
```
The mandatory keywords are:

- db_name: The name of the database you would like to save the SQL
- channel: The name of the channel from which to download data. Keep in mind that you need to register for the channel before downloading.
- topic: The topic of the channel. Valid topic is now `MVT` only.
- schema: The data schema. THose can be found in wiki, and maybe you are not into all columns/features, so just define the columns of features you want to download.
- username/password: If you save them as environment variable with `DATAFEED_USERNAME` and `DATAFEED_PW`, then they will be automatically uploaded. Otherwise, you have to define it in initialization.

This tool also provides a function that allows you to convert the downloaded SQL table into pandas Dataframe. You can achieve this by doing:
```
train_mv_rdf.to_pandas()
```
