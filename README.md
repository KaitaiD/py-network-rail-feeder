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

## Topics to download and store

There are four topics the readers can choose to download and store from Network Rail data feeds. Namely:

1. MVT - Train movement
2. PPM - Public performance measure
3. VSTP - Very short term planning
4. TD - Train describer

__Before running the script, readers must register and subscribe the corresponding feeds.__ Moreover, there is also a topic called 'SCHEDULE' that can be downloaded in a similar way to VSTP, however, it requires extra authorisation to access to the files. If interested, readers can gain the access and follow the similar step to complete the download.

## How to use it?

An example is given in the `example.py` and Train Movement is chosen as the topic I want to download.

For instance:

```python
TOPIC = 'MVT'


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
