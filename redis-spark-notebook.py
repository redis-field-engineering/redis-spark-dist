# Databricks notebook source
# MAGIC %md # Connect Spark with Redis Cloud
# MAGIC Spark and Redis together unlock powerful capabilities for data professionals. This guide demonstrates how to integrate these technologies for enhanced analytics, real-time processing, and machine learning applications.
# MAGIC
# MAGIC In this hands-on notebook, you'll learn how to make efficient use of Redis data structures alongside Spark's distributed computing framework. You'll see firsthand how to extract data from Redis, process it in Spark, and write results back to Redis for application use. Key topics include:
# MAGIC 1. Setting up the Spark-Redis connector in Databricks
# MAGIC 2. Writing data to Redis from Spark
# MAGIC 3. Reading data from Redis for application access
# MAGIC
# MAGIC ## Databricks Cluster Setup with Redis Connector
# MAGIC
# MAGIC 1. Set up a new Databricks cluster
# MAGIC 1. Go to the cluster's **Libraries** section
# MAGIC 1. Select **Install New**
# MAGIC 1. Choose **Maven** as your source and click **Search Packages**
# MAGIC 1. Enter `redis-spark-connector`` and select `com.redis:redis-spark-connector:x.y.z`
# MAGIC 1. Finalize by clicking **Install** <br/>
# MAGIC Want to explore the connector's full capabilities? Check the [detailed documentation](https://redis-field-engineering.github.io/redis-spark)
# MAGIC
# MAGIC ## Loading Test Data into Spark
# MAGIC 
# MAGIC In this step, you import a CSV file into your Unity Catalog volume. This is a shortened version of the [Import and visualize CSV data](https://docs.databricks.com/aws/en/getting-started/import-visualize-data) notebook.
# MAGIC 1. Replace `<catalog-name>`, `<schema-name>`, and `<volume-name>` with the catalog, schema, and volume names for a Unity Catalog volume. Optionally replace the `table_name` value with a table name of your choice.

# COMMAND ----------

catalog = "<catalog_name>"
schema = "<schema_name>"
volume = "<volume_name>"
download_url = "https://health.data.ny.gov/api/views/jxy9-yhdk/rows.csv"
file_name = "baby_names.csv"
table_name = "baby_names"
path_volume = "/Volumes/" + catalog + "/" + schema + "/" + volume
path_table = catalog + "." + schema
dbutils.fs.cp(f"{download_url}", f"{path_volume}" + "/" + f"{file_name}")
df = spark.read.csv(f"{path_volume}/{file_name}", header=True, inferSchema=True, sep=",")

# COMMAND ----------

# MAGIC %md ## Setting Up Redis Cloud Environment
# MAGIC
# MAGIC Redis Cloud offers a fully-managed Redis service ideal for this integration. Follow these steps:
# MAGIC
# MAGIC 1. Register for a [Redis Cloud account](https://redis.io/cloud/)
# MAGIC 1. Follow the [quickstart guide](https://redis.io/docs/latest/operate/rc/rc-quickstart/) to create a free tier database
# MAGIC
# MAGIC ## Configuring Spark with Redis Connection Details
# MAGIC
# MAGIC 1. From your Redis Cloud database dashboard, find your connection endpoint under **Connect**. The string follows this pattern: `redis://<user>:<pass>@<host>:<port>`
# MAGIC 1. In Databricks, open your cluster settings and locate **Advanced Options**. Under **Spark** in the **Spark config** text area, add your Redis connection string as both `spark.redis.read.connection.uri redis://...` and `spark.redis.write.connection.uri redis://...` parameters. This configuration applies to all notebooks using this cluster.
# MAGIC

# MAGIC ## Writing Data to Redis
# MAGIC
# MAGIC Let's use the `df` test data we imported earlier and write it to Redis.  
# MAGIC

# COMMAND ----------

df.write.format("redis").mode("overwrite").option("type", "hash").option("keyspace", "baby").option("key", "First Name").save()

# COMMAND ----------

# MAGIC %md ## Exploring Your Redis Data
# MAGIC Examine the keys and values you've created using **RedisInsight**, Redis' visual data browser. From your Redis Cloud database dashboard, click on **Redis Insight** and explore the data imported from Spark.  

# MAGIC ## Reading from Redis
# MAGIC
# MAGIC We can now read the data from Redis using the following line.
# MAGIC

# COMMAND ----------

redisDF = spark.read.format("redis").load()
display(redisDF)

# COMMAND ----------
