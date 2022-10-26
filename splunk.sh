#!/bin/bash

set -e
set -o pipefail

# These environment variables would normally be set by Spark scripts
# However, for a Databricks init script, they have not been set yet.
# We will keep the names the same here, but not export them.
# These must be changed if the associated Spark environment variables
# are changed.
DB_HOME=/databricks
SPARK_HOME=$DB_HOME/spark
SPARK_CONF_DIR=$SPARK_HOME/conf
export HOSTNAME


echo "Copying Spark Monitoring jars"
unzip /dbfs/FileStore/splunk/splunk_dependencies.zip -d /tmp/
cp -f /tmp/splunk_dependencies/* /mnt/driver-daemon/jars
rm -rf /tmp/splunk_dependencies

log4jDirectories=( "executor" "driver" "master-worker" "chauffeur")
for log4jDirectory in "${log4jDirectories[@]}"
do

LOG4J_CONFIG_FILE="$SPARK_HOME/dbconf/log4j/$log4jDirectory/log4j2.xml"
echo "BEGIN: Updating $LOG4J_CONFIG_FILE with SplunkHttp appender"
python /dbfs/FileStore/splunk/splunk_appender.py -i ${LOG4J_CONFIG_FILE} -o ${LOG4J_CONFIG_FILE}

echo "END: Updating $LOG4J_CONFIG_FILE with SplunkHttp appender"

done
