package com.lytrax.accessconverter;

import com.healthmarketscience.jackcess.Column;
import com.healthmarketscience.jackcess.Database;
import com.healthmarketscience.jackcess.Row;
import com.healthmarketscience.jackcess.Table;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.Date;
import java.util.HashMap;
import java.util.Locale;
import java.util.Map;
import java.util.Set;
import java.util.List;
import java.util.Arrays;
import org.apache.commons.text.TextStringBuilder;

/**
 *
 * @author Christos Lytras <christos.lytras@gmail.com>
 * @author Evyatar Kafkafi <evyatar@tamuz.org.il>
 */
public class MySQLConverter extends Converter {
    public final String DefaultCollate = "utf8mb4_unicode_ci";
    public final String DefaultCharset = "utf8mb4";
    public final String DefaultEngine = "InnoDB";

    public String collate = DefaultCollate;
    public String charset = DefaultCharset;
    public String engine = DefaultEngine;

    public class AutoIncrement {
        public int maxId = 0;
        public String columnName;
        public String tableName;
        public void setMaxId(int newMaxId) {
            maxId = Math.max(maxId, newMaxId);
        }
    }
    
    public Database db;
    public Args args;

    public Map<String, AutoIncrement> autoIncrements = new HashMap<>();
    public TextStringBuilder sqlDump;

    public Map<String, Integer> maxRowsInTable = new HashMap<>();

    public MySQLConverter(Args args, Database db) {
        this.args = args;
        this.db = db;
    }

    /**
     * Convert the accdb file to SQL INSERT statements
     * @return boolean Success
     */
    public boolean toMySQLDump() {
        boolean result = false;
        final String methodName = "toMySQLDump";
        List<String> exceptTheseTables = Arrays.asList(
            new String[]{
                        //"ComputationMethodData", // < - - too big even alone!
                        //"TariffDetailsHistory_777"
                        });
        List<String> onlyTheseTables = Arrays.asList(
            new String[]{//"ComputationMethodData",
                        //"TariffDetailsHistory_777"  // fields Title and TariffNote are . This table alone is 1.8GB! (2.3M rows)
                        });
        // the following is required for very big tables - it causes sqlDump to be written to stdout
        // without waiting for the end of the table. You'll get an Exception OutOfMemoryError if the numbers
        // are not low enough. These numbers were reached with trial and error, when app is run with -Xmx10g.
        maxRowsInTable.put("ComputationMethodData", 1_000_000); // exception in row 3327967
        maxRowsInTable.put("TariffDetailsHistory_777", 1_000_000);  // it has 2.3M rows
        try {
            sqlDump = new TextStringBuilder();
            addHeader();
            Set<String> tableNames = db.getTableNames();
            int count = 0 ;
            for (String tableName : tableNames) {
                try {
                    count = count + 1;
                    if (!onlyTheseTables.isEmpty()) {
                        // onlyTheseTables has names - do only those tables!!
                        if (!onlyTheseTables.contains(tableName)) {
                            continue;
                        }
                    }
                    else if (exceptTheseTables.contains(tableName)) {
                        continue;
                    }
                    System.out.println("-- add table " + tableName + ", sqlDump length=" + sqlDump.length());
                    Table table = db.getTable(tableName);
                    addTableCreate(table);
                    addTableInsert(table);
                    addAutoIncrements();
                } catch(IOException e) {
                    Error(String.format("Could not load table '%s'", tableName), e, methodName);
                }
            }
            
            addFooter();
            result = true;
        } catch(IOException e) {
            Error("Could not fetch tables from the database", e, methodName);
        }
        
        return result;
    }

    private void addHeader() {
        sqlDump.appendln(String.format("-- %s", Application.Title));
        sqlDump.appendln(String.format("-- version %s", Application.Version));
        sqlDump.appendln(String.format("-- author %s", Application.Author));
        sqlDump.appendln(String.format("-- %s", Application.Web));
        sqlDump.appendln("--");
        LocalDateTime datetime = LocalDateTime.now();
        Locale locale = new Locale("en", "US");
        sqlDump.appendln(String.format("-- Generation time: %s", datetime.format(DateTimeFormatter.ofPattern("EEE d, yyyy 'at' hh:mm a", locale))));
        sqlDump.appendNewLine();
        
        sqlDump.appendln("SET SQL_MODE = \"NO_AUTO_VALUE_ON_ZERO\";");
        sqlDump.appendln("SET AUTOCOMMIT = 0;");
        sqlDump.appendln("START TRANSACTION;");
        sqlDump.appendln("SET time_zone = \"+00:00\";");
        
        sqlDump.appendNewLine();
        sqlDump.appendNewLine();
        
        sqlDump.appendln("/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;");
        sqlDump.appendln("/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;");
        sqlDump.appendln("/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;");
        sqlDump.appendln(String.format("/*!40101 SET NAMES %s */;", charset));
        sqlDump.appendNewLine();
    }
    
    private void addFooter() {
        sqlDump.appendln("COMMIT;");
        sqlDump.appendNewLine();
        
        sqlDump.appendln("/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;");
        sqlDump.appendln("/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;");
        sqlDump.appendln("/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;");
        sqlDump.appendNewLine();
    }
    
    private void addTableCreate(Table table) {
        if(args.HasFlag("mysql-drop-tables")) {
            sqlDump.appendln("--");
            sqlDump.appendln(String.format("-- Drop table `%s` if exists", table.getName()));
            sqlDump.appendln("--");
            sqlDump.appendNewLine();
            sqlDump.appendln(String.format("DROP TABLE IF EXISTS `%s`;", table.getName()));
            sqlDump.appendNewLine();
        }
        
        sqlDump.appendln("--");
        sqlDump.appendln(String.format("-- Table structure for table `%s`", table.getName()));
        sqlDump.appendln("--");
        sqlDump.appendNewLine();
        
        sqlDump.appendln(String.format("CREATE TABLE IF NOT EXISTS `%s` (", table.getName()));
        
        boolean isFirst = true;
        
        for(Column column : table.getColumns()) {
            String name = column.getName();
            String type = column.getType().toString().toUpperCase();
            short length = column.getLength();
            
            if(!isFirst)
                sqlDump.appendln(",");
            else
                isFirst = false;
            
            switch(type) {
                case "BYTE":
                case "INT":
                case "LONG":
                    if(column.isAutoNumber()) {
                        AutoIncrement autoIncrement = new AutoIncrement();
                        autoIncrement.tableName = table.getName();
                        autoIncrement.columnName = name;
                        autoIncrements.put(autoIncrement.tableName, autoIncrement);
                        sqlDump.append(String.format("  `%s` INT(10) UNSIGNED NOT NULL", name));
                    } else {
                        switch(length) {
                            case 1:
                                sqlDump.append(String.format("  `%s` TINYINT(3) NOT NULL DEFAULT '0'", name));
                                break;
                            case 2:
                                sqlDump.append(String.format("  `%s` SMALLINT(5) NOT NULL DEFAULT '0'", name));
                                break;
                            case 4:
                                sqlDump.append(String.format("  `%s` INT(10) NOT NULL DEFAULT '0'", name));
                                break;
                            case 6:
                                sqlDump.append(String.format("  `%s` INT(10) NOT NULL DEFAULT '0'", name));
                                break;
                            default:
                                break;
                        }
                    }
                    break;
                case "FLOAT":
                    sqlDump.append(String.format("  `%s` FLOAT NOT NULL DEFAULT '0'", name));
                    break;
                case "DOUBLE":
                    sqlDump.append(String.format("  `%s` DOUBLE NOT NULL DEFAULT '0'", name));
                    break;
                case "NUMERIC":
                    sqlDump.append(String.format("  `%s` DECIMAL(28,0) NOT NULL DEFAULT '0'", name));
                    break;
                case "MONEY":
                    sqlDump.append(String.format("  `%s` DECIMAL(15,4) NOT NULL DEFAULT '0'", name));
                    break;
                case "BOOLEAN":
                    sqlDump.append(String.format("  `%s` TINYINT(3) NOT NULL DEFAULT '0'", name));
                    break;
                case "SHORT_DATE_TIME":
                    sqlDump.append(String.format("  `%s` DATETIME NOT NULL DEFAULT '0000-00-00 00:00:00'", name));
                    break;
                case "MEMO":
                    sqlDump.append(String.format("  `%s` TEXT COLLATE %s", name, collate));
                    break;
                case "GUID":
                    sqlDump.append(String.format("  `%s` VARCHAR(50) COLLATE %s DEFAULT '{00000000-0000-0000-0000-000000000000}'", name, collate));
                    break;
                case "TEXT":
                default:
                    sqlDump.append(String.format("  `%s` VARCHAR(255) COLLATE %s DEFAULT ''", name, collate));
                    break;
            }
        }
        
        sqlDump.appendNewLine();
        sqlDump.appendln(String.format(") ENGINE=%s DEFAULT CHARSET=%s COLLATE=%s;", engine, charset, collate));
        sqlDump.appendNewLine();
    }
    
    public static Integer defaultIfNullInteger(Integer i, int defaultValue) {
        if(i == null)
            return defaultValue;
        else
            return i;
    }

    public static Short defaultIfNullShort(Short i, int defaultValue) {
        if(i == null)
            return (short) defaultValue;
        else
            return i;
    }

    private void addTableInsert(Table table) {
        if(table.getRowCount() == 0)
            return;
        
        String tableName = table.getName();
        
        sqlDump.appendln("--");
        sqlDump.appendln(String.format("-- Dumping data for table `%s`", tableName));
        sqlDump.appendln("--");
        sqlDump.appendNewLine();
        
        TextStringBuilder insertHeader = new TextStringBuilder();
        insertHeader.append(String.format("INSERT INTO `%s` (", tableName));
        boolean isFirst = true;
        
        for(Column column : table.getColumns()) {
            if(!isFirst)
                insertHeader.append(", ");
            else
                isFirst = false;
            insertHeader.append(String.format("`%s`", column.getName()));
        }
        
        insertHeader.appendln(") VALUES");

        boolean isFirstColumn;
        //int insertRows = 0;
        int rowsCounter = 0 ;
        
        for(Row row : table) {
            rowsCounter = rowsCounter + 1;
//            if (maxRowsInTable.containsKey(tableName) && rowsCounter > maxRowsInTable.get(tableName)) {
//                break;
//            }

            TextStringBuilder insertValues = new TextStringBuilder();

            isFirstColumn = true;
            insertValues.append("(");
            
            for(Column column : table.getColumns()) {
                String type = column.getType().toString().toUpperCase();
                String name = column.getName();
                
                if(!isFirstColumn)
                    insertValues.append(", ");
                else
                    isFirstColumn = false;
                
                try {
                    switch(type) {
                        case "BYTE":
                            insertValues.append(row.getByte(name));
                            break;
                        case "INT":
                            insertValues.append(defaultIfNullShort(row.getShort(name), 0));
                            break;
                        case "LONG":
                            if(column.isAutoNumber() && autoIncrements.containsKey(tableName))
                                autoIncrements.get(tableName).setMaxId(row.getInt(name));
                            insertValues.append(defaultIfNullInteger(row.getInt(name), 0));
                            break;
                        case "FLOAT":
                            insertValues.append(row.getFloat(name));
                            break;
                        case "DOUBLE":
                            insertValues.append(Globals.defaultIfNullDouble(row.getDouble(name)));
                            break;
                        case "NUMERIC":
                        case "MONEY":
                            insertValues.append(row.getBigDecimal(name));
                            break;
                        case "BOOLEAN":
                            insertValues.append(row.getBoolean(name) ? 1 : 0);
                            break;
                        case "SHORT_DATE_TIME":
                            Date d = row.getDate(name);
                            if (d == null) {
                                d = new Date(0);
                            }
                            SimpleDateFormat format = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
                            String val = String.format("'%s'", format.format(d));
                            insertValues.append(val);
                            break;
                        case "MEMO":
                        case "GUID":
                        case "TEXT":
                            // need special handling for TEXT values that are RTF, because \ ' b 3 causes crashes in import
                            String val2 = row.getString(name);
                            if (val2 == null) {
                                insertValues.append("'TEMPORARILY_NULL'");
                            }
                            else if (name.endsWith("RTF")) {
                                // temporary solution!! it will damage RTF content in unknown ways!!
                                // temporary solution!! completely delete RTF values
                                insertValues.append("'TEMPORARILY_REMOVED_RTF'");
                            }
                            else {
                                insertValues.append(String.format("'%s'", val2.replace("'", "''")));
                            }
                            
                            break;
                        case "COMPLEX_TYPE":
                        default:
                            insertValues.append("'UNKNOWN_TYPE_REMOVED'");
                            break;
                    }
                } catch(NullPointerException e) {
                    insertValues.append("'EXCEPTION_REMOVED'");
                }
            }
            
            insertValues.append(")");
            insertValues.appendln(";");

            try {
                if (maxRowsInTable.containsKey(tableName) && rowsCounter > maxRowsInTable.get(tableName)) {
                    // do not append to sqlDump, because it will cause OutOfMemory

                    // dump sqlDump and start counting again
                    dumpToStdout(sqlDump);
                    sqlDump = null; // This should GC anything collected in sqlDump until now
                    sqlDump = new TextStringBuilder();
                    rowsCounter = 0 ;   // start counting again
                }
                //else {
                {   // now this should be done in all cases, not just the else of the above if
                    sqlDump.append(insertHeader);
                    sqlDump.append(insertValues);
                }
            }
            catch (Exception ex) {
                System.out.println("-- absorbing Exception " + ex.getMessage() + " in table " + tableName + " in row " + rowsCounter);
                break;  // out of loop of rows for the current table
            }
        }

    }
    
    public void addAutoIncrements() {
        for(AutoIncrement autoIncrement : autoIncrements.values()) {
            sqlDump.appendln("--");
            sqlDump.appendln(String.format("-- Indexes for table `%s`", autoIncrement.tableName));
            sqlDump.appendln("--");
            sqlDump.appendln(String.format("ALTER TABLE `%s`", autoIncrement.tableName));
            sqlDump.appendln(String.format("  ADD PRIMARY KEY (`%s`);", 
                    autoIncrement.columnName));
            
            sqlDump.appendNewLine();
            
            sqlDump.appendln("--");
            sqlDump.appendln(String.format("-- AUTO_INCREMENT for table `%s`", autoIncrement.tableName));
            sqlDump.appendln("--");
            sqlDump.appendln(String.format("ALTER TABLE `%s`", autoIncrement.tableName));
            sqlDump.appendln(String.format("  MODIFY `%s` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=%d;", 
                    autoIncrement.columnName, 
                    autoIncrement.maxId + 1));
        }
        sqlDump.appendNewLine();
    }

    private static void dumpToStdout(TextStringBuilder sqlDump) {
        int length = sqlDump.length();
        System.out.println("-- dumpToStdout 1, length=" + length);
        int STEP = 10000000;
        int index = STEP ;
        int prev = 0;
        while (index < length) {
            String strPart = sqlDump.substring(prev, index);
            System.out.println(strPart);
            prev = index;
            index = index + STEP;
        }
        String strPart = sqlDump.substring(prev, length);
        System.out.println(strPart);
    }
}
