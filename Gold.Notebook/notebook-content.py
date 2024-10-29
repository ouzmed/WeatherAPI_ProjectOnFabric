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

# #### Preparing datamart tables

# CELL ********************

from pyspark.sql.functions import col, mean, round

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df = spark.sql("SELECT * FROM lakehouse_meteo.silver_tbl")
display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_idf = df.filter(col("region") == 'Ile-de-France').select("city", "temperature", "felt","is_day","last_updated")
df_MED = df.where(col("region") == 'Provence-Alpes-Cote d\'Azur').select("city", "temperature", "felt","is_day","last_updated")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_agg = df.groupBy("region").agg(round(mean("temperature"),2).alias("temp_avg"))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

display(df_agg)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_idf.write.format("delta").mode("overwrite").saveAsTable("lakehouse_meteo.idf_meteo")
df_MED.write.format("delta").mode("overwrite").saveAsTable("lakehouse_meteo.med_meteo")
df_agg.write.format("delta").mode("overwrite").saveAsTable("lakehouse_meteo.temp_avg_per_region")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
