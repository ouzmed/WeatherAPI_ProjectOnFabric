# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "c89d9cff-8219-417e-b08d-150a15ff1462",
# META       "default_lakehouse_name": "lakehouse_meteo",
# META       "default_lakehouse_workspace_id": "de70c26b-d4a5-4ecb-b5ba-1d59aee2cbef",
# META       "known_lakehouses": [
# META         {
# META           "id": "c89d9cff-8219-417e-b08d-150a15ff1462"
# META         }
# META       ]
# META     }
# META   }
# META }

# MARKDOWN ********************

# #### Import necessary libraries

# CELL ********************

from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DecimalType, FloatType
import requests
import json


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# #### Creating a function to call API and fetch data

# CELL ********************

# def a function to call the api and fetch the data

def get_data(url, headers):

    response = requests.get(url, headers)
    if response.status_code == 200:
        
        return response.json()
        #print(data_jsn)
    
    else:
        print(f"Error with the code {response.status_code}: {response.text}")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# #### Example of an endpoint

# CELL ********************

# the api key, for the security it's important to secure it inside for example key vault

key = "1967578b90254ad29e594056242910"
url = f"http://api.weatherapi.com/v1/current.json?key={key}&q=Toulouse&aqi=no"
headers = {
    'accept': 'application/json'
    }
example = get_data(url, headers=headers)
print(example)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# #### Creating the dataframe which will containe the meteo data of some countries in France

# CELL ********************


cities = ['Paris', 'Toulouse', 'Lyon', 'Bourdeaux', 'Nice', 'Lille', 'Strasbourg','Marseille', 'Nantes']

name=[]
region=[]
country=[]
latitude=[]
longitude=[]
last_updated=[]
temp_c=[]
is_day=[]
wind_degree=[]
humidity=[]
cloud=[]
windchill_c=[]

for city in cities:
    
    url1 = f"http://api.weatherapi.com/v1/current.json?key={key}&q={city}&aqi=no"
    data_ = get_data(url1, headers = headers)

    name.append(data_['location']['name'])
    region.append(data_['location']['region'])
    latitude.append(data_['location']['lat'])
    longitude.append(data_['location']['lon'])
    last_updated.append(data_['current']['last_updated'])
    temp_c.append(data_['current']['temp_c'])
    is_day.append(data_['current']['is_day'])
    wind_degree.append(data_['current']['wind_degree'])
    humidity.append(data_['current']['humidity'])
    cloud.append(data_['current']['cloud'])
    windchill_c.append(data_['current']['windchill_c'])


data = list(zip(name, region, latitude, longitude, last_updated, temp_c, is_day, wind_degree, humidity, cloud, windchill_c))


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# #### Creating the schema

# CELL ********************

# define the schema for the dataframe

schema = StructType([
    StructField('name', StringType(), True),
    StructField('region', StringType()),
    StructField('latitude', FloatType()),
    StructField('longitude', FloatType()),
    StructField('last_updated', StringType()),
    StructField('temp_c', FloatType()),
    StructField('is_day', IntegerType()),
    StructField('wind_degree', IntegerType()),
    StructField('humidity', IntegerType()),
    StructField('cloud', IntegerType()),
    StructField('windchill_c', FloatType()),
])


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# #### DATAFRAME df

# CELL ********************

# define the dataframe

df = spark.createDataFrame(data=data, schema=schema)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Display the dataframe

display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df.write.format("delta").mode("overwrite").saveAsTable("Lakehouse_meteo.bronze_tbl")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
