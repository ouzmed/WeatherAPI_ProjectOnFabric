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
# META       "default_lakehouse_workspace_id": "de70c26b-d4a5-4ecb-b5ba-1d59aee2cbef"
# META     }
# META   }
# META }

# MARKDOWN ********************

# #### Preparing Silver Table

# CELL ********************

from pyspark.sql.functions import col, cast, when

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df = spark.sql("SELECT * FROM lakehouse_meteo.bronze_tbl")
display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************


df.printSchema()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# cleaning the data type of the columns and changing the content of the column is_day

df_dt = df.withColumn("last_updated", col("last_updated").cast("date"))\
          .withColumn("is_day", when(col("is_day") == 1, "day").otherwise("night"))

display(df_dt)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# rename the columns with a significant names:

df_cleaned = df_dt.withColumnRenamed("name","city")\
                .withColumnRenamed("temp_c", "temperature")\
                .withColumnRenamed("windchill_c", "felt")
display(df_cleaned)              

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# #### Saving the refined dataframe into a silver table in the lakehouse 

# CELL ********************

df_cleaned.write.format("delta").mode("overwrite").saveAsTable("lakehouse_meteo.silver_tbl")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
