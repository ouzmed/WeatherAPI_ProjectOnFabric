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

df = spark.sql("SELECT * FROM lakehouse_meteo.bronze_tbl")
display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************




# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
