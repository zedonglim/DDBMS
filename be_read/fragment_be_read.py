import pymysql


# Connect to your MySQL database
connection = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='TAN@mysql',
    database='dmbs1',
    port=3306
)

# Create a cursor object to execute SQL queries
cursor = connection.cursor()

# Query the user, article, and read tables
cursor.execute("SELECT aid FROM article;")
aid = cursor.fetchall()
aid_list = [id[0] for id in aid]

connection.close()

# Read the SQL file
with open('be_read/be_read_dbms2.sql', 'r') as file:
    sql_statements = file.read()

# Find the start of the insert statement
start = sql_statements.index("INSERT INTO `be_read` (`timestamp`, `aid`, `readNum`, `readUidList`, `commentNum`, `commentUidList`, `agreeNum`, `agreeUidList`, `shareNum`, `shareUidList`) VALUES")

# Get the insert statement
insert_statement = sql_statements[start:]

# Split the insert statement into individual rows
rows = insert_statement.split('\n')

print(rows[1])

# Separate the rows for dbms1 and dbms2
dbms1_rows = []
i = 0
for row in rows:
    if i == 0:
        i += 1
        continue
    if i == len(rows) - 1:
        break
    new_row = row.split('"')
    # print(new_row)
    id = new_row[3]
    if id in aid_list:
        dbms1_rows.append(row+"\n")
    i += 1


# Write the dbms1 SQL file
with open('be_read_dbms1.sql', 'w') as file:
    file.write("DROP TABLE IF EXISTS `be_read`;\n")
    file.write("CREATE TABLE `be_read` (\n" + \
            "  `id` bigint NOT NULL AUTO_INCREMENT,\n" + \
            "  `timestamp` text DEFAULT NULL,\n" + \
            "  `aid` char(7) DEFAULT NULL,\n" + \
            "  `readNum` bigint DEFAULT NULL,\n" +  \
            "  `readUidList` text,\n" +  \
            "  `commentNum` bigint DEFAULT NULL,\n" +  \
            "  `commentUidList` text,\n" +  \
            "  `agreeNum` bigint DEFAULT NULL,\n" +  \
            "  `agreeUidList` text,\n" +  \
            "  `shareNum` bigint DEFAULT NULL,\n" +  \
            "  `shareUidList` text,\n" + \
            "  PRIMARY KEY (`id`),\n" + \
            "  CONSTRAINT `fk_be_read_aid` FOREIGN KEY (`aid`) REFERENCES `article` (`aid`)\n" + \
            ") ENGINE=InnoDB DEFAULT CHARSET=utf8;\n\n")
    file.write("LOCK TABLES `be_read` WRITE;\n")
    file.write('INSERT INTO `be_read` (`timestamp`, `aid`, `readNum`, `readUidList`, `commentNum`, `commentUidList`, `agreeNum`, `agreeUidList`, `shareNum`, `shareUidList`) VALUES\n' + "".join(dbms1_rows) + ';')
    file.write("UNLOCK TABLES;")
