@echo off
rem 
rem Run AnyLogic Experiment
rem 
chcp 1252 >nul 
set DIR_BACKUP_XJAL=%cd%
cd /D "%~dp0"
set DISK_XJAL=C:
set OPTIONS_XJAL=
if not [%SystemDrive%]==[] set DISK_XJAL=%SystemDrive%
set PATH_XJAL="%DISK_XJAL%\Program Files\Java\jre8\bin\java.exe"
for /f "delims=" %%a in ('dir "%ProgramFiles%\Java\jre-9*" /on /ad /b') do (
	set PATH_XJAL="%ProgramFiles%\Java\%%a\bin\java.exe"
	set OPTIONS_XJAL=--illegal-access=deny
)
if not exist %PATH_XJAL% set PATH_XJAL="%ProgramFiles%\Java\jre8\bin\java.exe"
if not exist %PATH_XJAL% set PATH_XJAL="%DISK_XJAL%\Program Files (x86)\Java\jre8\bin\java.exe"
if not exist %PATH_XJAL% set PATH_XJAL="%DISK_XJAL%\Program Files (x86)\Java\jre1.8.0_191\bin\java.exe"
if not exist %PATH_XJAL% set PATH_XJAL="%ProgramFiles(x86)%\Java\jre8\bin\java.exe"
if not exist %PATH_XJAL% set PATH_XJAL="%JAVA_HOME%\bin\java.exe"
if not exist %PATH_XJAL% set PATH_XJAL=java
echo on
%PATH_XJAL% %OPTIONS_XJAL% -cp model.jar;lib/ProcessModelingLibrary.jar;lib/MaterialHandlingLibrary.jar;lib/FluidLibrary.jar;lib/commons-math3-3.3.jar;lib/com.anylogic.engine.jar;lib/com.anylogic.engine.nl.jar;lib/com.anylogic.engine.sa.jar;lib/sa/com.anylogic.engine.sa.web.jar;lib/sa/executor-basic-8.3.jar;lib/sa/ioutil-8.3.jar;lib/sa/spark/commons-codec-1.10.jar;lib/sa/spark/jackson-annotations-2.8.5.jar;lib/sa/spark/jackson-core-2.8.5.jar;lib/sa/spark/jackson-databind-2.8.5.jar;lib/sa/spark/jackson-datatype-jsr310-2.8.5.jar;lib/sa/spark/javax.servlet-api-3.1.0.jar;lib/sa/spark/jetty-client-9.4.8.v20171121.jar;lib/sa/spark/jetty-http-9.4.8.v20171121.jar;lib/sa/spark/jetty-io-9.4.8.v20171121.jar;lib/sa/spark/jetty-security-9.4.8.v20171121.jar;lib/sa/spark/jetty-server-9.4.8.v20171121.jar;lib/sa/spark/jetty-servlet-9.4.8.v20171121.jar;lib/sa/spark/jetty-servlets-9.4.8.v20171121.jar;lib/sa/spark/jetty-util-9.4.8.v20171121.jar;lib/sa/spark/jetty-webapp-9.4.8.v20171121.jar;lib/sa/spark/jetty-xml-9.4.8.v20171121.jar;lib/sa/spark/jsch-0.1.54.jar;lib/sa/spark/slf4j-api-1.7.21.jar;lib/sa/spark/spark-core-2.7.2.jar;lib/sa/spark/websocket-api-9.4.8.v20171121.jar;lib/sa/spark/websocket-client-9.4.8.v20171121.jar;lib/sa/spark/websocket-common-9.4.8.v20171121.jar;lib/sa/spark/websocket-server-9.4.8.v20171121.jar;lib/sa/spark/websocket-servlet-9.4.8.v20171121.jar;lib/sa/util-8.3.jar;lib/OptQuest.jar;lib/database/querydsl/querydsl-core-3.6.3.jar;lib/database/querydsl/querydsl-sql-3.6.3.jar;lib/database/querydsl/querydsl-sql-codegen-3.6.3.jar;lib/database/anylogic_database.jar;lib/database/bcprov-jdk15-1.46.jar;lib/database/commons-lang-2.6.jar;lib/database/commons-logging-1.1.1.jar;lib/database/hsqldb.jar;lib/database/jackcess-2.0.6.jar;lib/database/jackcess-encrypt-2.0.2.jar;lib/database/jsqlparser-0.9.5.jar;lib/database/jtds-1.3.1.jar;lib/database/querydsl/annotation-indexer-1.2.jar;lib/database/querydsl/ant-1.8.1.jar;lib/database/querydsl/ant-launcher-1.8.1.jar;lib/database/querydsl/bridge-method-annotation-1.13.jar;lib/database/querydsl/codegen-0.6.6.jar;lib/database/querydsl/geolatte-geom-0.13.jar;lib/database/querydsl/guava-18.0.jar;lib/database/querydsl/javax.inject-1.jar;lib/database/querydsl/joda-time-1.6.jar;lib/database/querydsl/jsr305-1.3.9.jar;lib/database/querydsl/jts-1.12.jar;lib/database/querydsl/log4j-1.2.16.jar;lib/database/querydsl/mysema-commons-lang-0.2.4.jar;lib/database/querydsl/ojdbc6-11.1.0.7.0.jar;lib/database/querydsl/org.apache.servicemix.bundles.javax-inject-1_2.jar;lib/database/querydsl/postgis-jdbc-1.3.3.jar;lib/database/querydsl/postgis-stubs-1.3.3.jar;lib/database/querydsl/postgresql-8.3-603.jdbc4.jar;lib/database/querydsl/querydsl-codegen-3.6.3.jar;lib/database/querydsl/querydsl-spatial-3.6.3.jar;lib/database/querydsl/sdoapi-11.2.0.jar;lib/database/querydsl/slf4j-api-1.6.1.jar;lib/database/querydsl/validation-api-1.1.0.Final.jar;lib/database/sqljdbc41.jar;lib/database/sqlsheet-6.6.jar;lib/database/ucanaccess-2.0.9.2.jar;lib/poi/dom4j-1.6.1.jar;lib/poi/poi-3.10.1-20140818.jar;lib/poi/poi-examples-3.10.1-20140818.jar;lib/poi/poi-excelant-3.10.1-20140818.jar;lib/poi/poi-ooxml-3.10.1-20140818.jar;lib/poi/poi-ooxml-schemas-3.10.1-20140818.jar;lib/poi/poi-scratchpad-3.10.1-20140818.jar;lib/poi/stax-api-1.0.1.jar;lib/poi/xmlbeans-2.6.0.jar;lib/ecj/ecj-4.7.1a.jar;lib/ecj/java9api.jar -Xmx1024m petPerfect1.Simulation %*
@cd /D "%DIR_BACKUP_XJAL%"
