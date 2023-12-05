# Read the SQL file
with open('user.sql', 'r') as file:
    sql_statements = file.read()

# Find the start of the insert statement
start = sql_statements.index('INSERT INTO `user` VALUES')

# Get the insert statement
insert_statement = sql_statements[start:]

# Split the insert statement into individual rows
rows = insert_statement.split('(')

print(rows[1])

# Separate the rows for dbms1 and dbms2
dbms1_rows = []
dbms2_rows = []

for row in rows:
    if "Beijing" in row:
        dbms1_rows.append("("+row)
    elif "Hong Kong" in row:
        dbms2_rows.append("("+row)

# Write the dbms1 SQL file
with open('user_dbms1.sql', 'w') as file:
    file.write("DROP TABLE IF EXISTS `user`;\n")
    file.write("CREATE TABLE `user` (\n" + \
            "  `timestamp` char(14) DEFAULT NULL,\n" + \
            "  `id` char(5) DEFAULT NULL,\n" + \
            "  `uid` char(5) DEFAULT NULL,\n" + \
            "  `name` char(9) DEFAULT NULL,\n" +  \
            "  `gender` char(7) DEFAULT NULL,\n" +  \
            "  `email` char(10) DEFAULT NULL,\n" +  \
            "  `phone` char(10) DEFAULT NULL,\n" +  \
            "  `dept` char(9) DEFAULT NULL,\n" +  \
            "  `grade` char(7) DEFAULT NULL,\n" +  \
            "  `language` char(3) DEFAULT NULL,\n" +  \
            "  `region` char(10) DEFAULT NULL,\n" +  \
            "  `role` char(6) DEFAULT NULL,\n" +  \
            "  `preferTags` char(7) DEFAULT NULL,\n" +  \
            "  `obtainedCredits` char(3) DEFAULT NULL\n) ENGINE=InnoDB DEFAULT CHARSET=utf8;\n\n")
    file.write("LOCK TABLES `user` WRITE;\n")
    file.write('INSERT INTO `user` VALUES\n' + "".join(dbms1_rows) + ';')

# Write the dbms2 SQL file
with open('user_dbms2.sql', 'w') as file:
    file.write("DROP TABLE IF EXISTS `user`;\n")
    file.write("CREATE TABLE `user` (\n" + \
            "  `timestamp` char(14) DEFAULT NULL,\n" + \
            "  `id` char(5) DEFAULT NULL,\n" + \
            "  `uid` char(5) DEFAULT NULL,\n" + \
            "  `name` char(9) DEFAULT NULL,\n" +  \
            "  `gender` char(7) DEFAULT NULL,\n" +  \
            "  `email` char(10) DEFAULT NULL,\n" +  \
            "  `phone` char(10) DEFAULT NULL,\n" +  \
            "  `dept` char(9) DEFAULT NULL,\n" +  \
            "  `grade` char(7) DEFAULT NULL,\n" +  \
            "  `language` char(3) DEFAULT NULL,\n" +  \
            "  `region` char(10) DEFAULT NULL,\n" +  \
            "  `role` char(6) DEFAULT NULL,\n" +  \
            "  `preferTags` char(7) DEFAULT NULL,\n" +  \
            "  `obtainedCredits` char(3) DEFAULT NULL\n) ENGINE=InnoDB DEFAULT CHARSET=utf8;\n\n")
    file.write("LOCK TABLES `user` WRITE;\n")
    file.write('INSERT INTO `user` VALUES\n' + ''.join(dbms2_rows) + ';')
