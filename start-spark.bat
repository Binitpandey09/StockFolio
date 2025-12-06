@echo off
echo ========================================
echo    🔥 Starting Apache Spark Shell 🔥
echo ========================================
echo.
echo ✅ Java 17 installed and configured
echo ✅ Spark 4.0.1 ready to use
echo ✅ Environment variables set
echo.
echo 💡 Tip: After restarting Command Prompt, you can simply type: spark-shell
echo.

set JAVA_HOME=C:\Program Files\Microsoft\jdk-17.0.16.8-hotspot
set SPARK_HOME=C:\spark-4.0.1-bin-hadoop3
set HADOOP_HOME=C:\winutils

"C:\spark-4.0.1-bin-hadoop3\bin\spark-shell.cmd" %*
echo.

"C:\spark-4.0.1-bin-hadoop3\spark-4.0.1-bin-hadoop3\bin\spark-shell.cmd" %*
