# Convert AccessDB
Note: all command line is Linux (Ubuntu 20.04). For Mac users it should be the same. Windows users should make the necessary adjustments.

## How to operate

### Prerequisites
- For running an already prepared JAR file, you need to install JDK 8 on your machine. (or JDK 11? the pom.xml compiles for 1.8, but it seems my JDK11 can run this)
  - Installing and using Java requires some experience. I recommend using `sdkman`, but you can also install JDK directly.
  - in command line do `java --version` to see if you have a JDK and what version it is.
- For building the JAR, you need to install Maven on your machine (Alternatively, if you already have the JAR file, you don't need Maven to execute it, only JDK)
  - in command line do `mvn --version` to see if you have Maven installed.

### building and executing
in command line - move to the correct sub-directory (it is the sub-directory that contains a `pom.xml` file)
```
cd ~/Documents/custom/GitHub/Customs_Book/AccessDB/AccessConverter
```
Building the code is done with Maven (which is the standard way for Java projects).
```
mvn package
```
if successful, it creates a (fat) JAR file in `./target` sub-directory.
To execute:
```
java -Xmx10g -jar ./target/access-converter-jar-with-dependencies.jar --access-file "/home/evyatar/Documents/custom/1/fullCustomsBookData/AccessDBTamplate20220411.accdb" --task convert-mysql-dump --output-file "/home/evyatar/Downloads/custom/3/somedb_dump.sql" --log-file "/home/evyatar/Documents/custom/3/somedb.log"  -mysql-drop-tables --output-result normal > /home/evyatar/Documents/custom/3/dump.sql
```

The resulting file is in `/home/evyatar/Documents/custom/3/dump.sql`. for an accdb file of 1.1GB, the dump.sql file is 3.9GB! (with all tables!). I have not yet tested if such a big file can be imported by MySQL.

### Fat Jar
The pom.xml instructs Maven to create a Fat Jar (uber-jar). This means all the dependent Jars are archived in one JAR that can be executed with `java -jar ...`

Maven-assembly-plugin is documented [here](https://maven.apache.org/plugins/maven-assembly-plugin/index.html) (current version at the time of writing is 3.3.0). There is an alternative way, with the [Maven Shade Plugin](https://maven.apache.org/plugins/maven-shade-plugin/), but for my purpose Maven-assembly-plugin is sufficient.
Maven-compiler-plugin is documented [here](https://maven.apache.org/plugins/maven-compiler-plugin/index.html) (current version at the time of writing is 3.10.1).

### Troubleshhooting
1. if the `mvn package` command does not work, try first `mvn --version` - just to see if that works
2. if `mvn` command is not recognized, you need to install Maven.
3. the first invocation of `mvn package` requires a long time (and a good internet connection), because Maven downloads a lot of "dependencies" from Maven Central.
4. The `java` command has `-Xmx10g` which requires a **lot** of memory (10 GB!). If your machine does not have so much memory, change it to `-Xmx1g` or any other value. The large amount of memory is required to convert the large accdb. If you have a smaller accdb file, you will need less memory
5. in the java command line you should change all paths to the correct paths on your machine.
6. the `/home/evyatar/.m2/` in the classpath assumes that your Maven has its local reposiroty at /home/evyatar/.m2 - this is its default (change `evyatar` to your user name!)
7. if you receive the following error message
```
Exception in thread "main" java.lang.OutOfMemoryError: Java heap space
	at java.base/java.util.Arrays.copyOf(Arrays.java:3745)
	at java.base/java.lang.AbstractStringBuilder.ensureCapacityInternal(AbstractStringBuilder.java:172)
	at java.base/java.lang.AbstractStringBuilder.append(AbstractStringBuilder.java:538)
	at java.base/java.lang.StringBuilder.append(StringBuilder.java:174)
```
it means that the memory allocated for the JVM is not enough. This is most probably because the accdb file is too big. You can allocate more memory by adding `-Xmx10g` to the command line (change 10g to whatever number suitable. The `g` denotes GigaBytes).


## Current restrictions
1. the code currently ignores columns with RTF (coulmn name ends with RTF) because it seems the Hebrew is not rendered correctly in the import file.
2. requires `-Xmx10g`!


## To Do
1. change code to create a separate SQL file for each table. Currently, some tables are still too big to handle properly.
2. change code to enable defining in arguments which table to convert



