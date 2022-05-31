# Convert AccessDB
Note: all command line is Linux (Ubuntu 20.04). For Mac users it should be the same. Windows users should make the necessary adjustments.

## How to operate

### Prerequisites
- For running an already prepared JAR file, you need to install JDK 8 on your machine.
  - Installing and using Java requires some experience. I recommend using `sdkman`, but you can also install JDK directly
  - in command line do `java --version` to see if you have a JDK and what version it is.
- For building the JAR, you need to install Maven on your machine (Alternatively, if you already have the JAR file, you don't need Maven to execute it, only JDK)
  - in command line do `mvn --version` to see if you have Maven installed.

### building and executing
in command line - move to the correct sub-directory (it is the sub-directory that contains a `pom.xml` file)
```
cd ~/Documents/custom/accessConverter/AccessConverter
```
Building the code is done with Maven (which is the standard way for Java projects).
```
mvn package
```
if successful, it creates a JAR file in `./target` sub-directory.
To execute:
```
java -Xmx28g -cp ./target/accessconverter-1.1.1.jar:/home/evyatar/.m2/repository/javax/json/javax.json-api/1.0/javax.json-api-1.0.jar:/home/evyatar/.m2/repository/commons-io/commons-io/2.5/commons-io-2.5.jar:/home/evyatar/.m2/repository/org/glassfish/javax.json/1.0.1/javax.json-1.0.1.jar:/home/evyatar/.m2/repository/com/healthmarketscience/jackcess/jackcess/2.1.8/jackcess-2.1.8.jar:/home/evyatar/.m2/repository/commons-logging/commons-logging/1.2/commons-logging-1.2.jar:/home/evyatar/.m2/repository/org/apache/commons/commons-lang3/3.6/commons-lang3-3.6.jar:/home/evyatar/.m2/repository/commons-lang/commons-lang/2.6/commons-lang-2.6.jar:/home/evyatar/.m2/repository/org/apache/commons/commons-text/1.3/commons-text-1.3.jar com.lytrax.accessconverter.AccessConverter --access-file "/home/evyatar/Downloads/custom/1/fullCustomsBookData/AccessDBTamplate20220411.accdb" --task convert-mysql-dump --output-file "/home/evyatar/Downloads/custom/3/somedb_dump.sql" --log-file "/home/evyatar/Downloads/custom/3/somedb.log"  -mysql-drop-tables --output-result normal > ../../3/dump.sql
```

The resulting file is in `../../3/dump.sql`

### Troubleshhooting
1. if the `mvn package` command does not work, try first `mvn --version` - just to see if that works
2. if `mvn` command is not recognized, you need to install Maven.
3. the first invocation of `mvn package` requires a long time (and a good internet connection), because Maven downloads a lot of "dependencies" from Maven Central.
4. The `java` command has `-Xmx28g` which requires a **lot** of memory (28 GB!). If your machine does not have so much memory, change it to `-Xmx1g` or any other value. The large amount of memory is required to convert the large accdb. If you have a smaller accdb file, you will need less memory
5. in the java command line you should change all paths to the correct paths on your machine.
6. I plan to change the pom.xml file to build a "fat" JAR, and then I wouldn't need to supply JARs in the classpath with the `-cp` .