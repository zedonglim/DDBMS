# connect to mysql and get user data
import pymysql
# Connect to your MySQL database
db1_connect = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='TAN@mysql',
    database='dmbs1',
    port=3306
)

cursor = db1_connect.cursor()

# Query the user, article, and read tables
cursor.execute("SELECT uid FROM user;")
users_id = cursor.fetchall()
id_list = [uid[0] for uid in users_id]

# Close the database connection
db1_connect.close()


# Read the SQL file
with open('user_read.sql', 'r') as file:
    sql_statements = file.read()

# Find the start of the insert statement
start = sql_statements.index('INSERT INTO `user_read` VALUES')

# Get the insert statement
insert_statement = sql_statements[start:]

# Split the insert statement into individual rows
rows = insert_statement.split('\n')

print(rows[1])

# Separate the rows for dbms1 and dbms2
dbms1_rows = []
dbms2_rows = []
i = 0
for row in rows:
    if i == 0:
        i += 1
        continue
    if i == len(rows) - 1:
        break
    new_row = row.split('"')
    # print(new_row)
    id = new_row[5]
    if id in id_list:
        dbms1_rows.append(row+"\n")
    else:
        dbms2_rows.append(row+"\n")
    i += 1

print(len(dbms1_rows))
# Write the dbms1 SQL file
with open('user_read_dbms1.sql', 'w') as file:
    file.write("DROP TABLE IF EXISTS `user_read`;\n")
    file.write("CREATE TABLE `user_read` (\n" + \
        "  `timestamp` char(14) DEFAULT NULL,\n" + \
        "  `id` char(7) DEFAULT NULL,\n" + \
        "  `uid` char(5) DEFAULT NULL,\n" + \
        "  `aid` char(7) DEFAULT NULL,\n" + \
        "  `readTimeLength` char(3) DEFAULT NULL,\n" +  \
        "  `agreeOrNot` char(2) DEFAULT NULL,\n" +  \
        "  `commentOrNot` char(2) DEFAULT NULL,\n" +  \
        "  `shareOrNot` char(2) DEFAULT NULL,\n" +  \
        "  `commentDetail` char(100) DEFAULT NULL\n) ENGINE=InnoDB DEFAULT CHARSET=utf8;\n\n")

    file.write("LOCK TABLES `user_read` WRITE;\n")
    file.write('INSERT INTO `user_read` VALUES\n' + "".join(dbms1_rows) + '\n')
    # file.write("UNLOCK TABLES;\n\n\n")
# Write the dbms2 SQL file
with open('user_read_dbms2.sql', 'w') as file:
     file.write("DROP TABLE IF EXISTS `user_read`;\n")
     file.write("CREATE TABLE `user_read` (\n" + \
            "  `timestamp` char(14) DEFAULT NULL,\n" + \
            "  `id` char(7) DEFAULT NULL,\n" + \
            "  `uid` char(5) DEFAULT NULL,\n" + \
            "  `aid` char(7) DEFAULT NULL,\n" + \
            "  `readTimeLength` char(3) DEFAULT NULL,\n" +  \
            "  `agreeOrNot` char(2) DEFAULT NULL,\n" +  \
            "  `commentOrNot` char(2) DEFAULT NULL,\n" +  \
            "  `shareOrNot` char(2) DEFAULT NULL,\n" +  \
            "  `commentDetail` char(100) DEFAULT NULL\n) ENGINE=InnoDB DEFAULT CHARSET=utf8;\n\n")

     file.write("LOCK TABLES `user_read` WRITE;\n")
     file.write('INSERT INTO `user_read` VALUES\n' + ''.join(dbms2_rows) + '\n')
    #  file.write("UNLOCK TABLES;\n\n\n")