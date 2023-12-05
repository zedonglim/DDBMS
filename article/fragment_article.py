import random
# Read the SQL file
with open('article_dmbs2.sql', 'r') as file:
    sql_statements = file.read()

# Find the start of the insert statement
start = sql_statements.index('INSERT INTO `article` VALUES')

# Get the insert statement
insert_statement = sql_statements[start:]

# Split the insert statement into individual rows
rows = insert_statement.split('(')

print(rows[1])

# Separate the rows for dbms1 and dbms2
dbms1_rows = []

for row in rows:
    if "science" in row:
        dbms1_rows.append("("+row)

# Write the dbms1 SQL file
with open('article_dbms1.sql', 'w') as file:
    file.write("DROP TABLE IF EXISTS `article`;\n")
    file.write("CREATE TABLE `article` (\n" + \
            "  `timestamp` char(14) DEFAULT NULL,\n" + \
            "  `id` char(7) DEFAULT NULL,\n" + \
            "  `aid` char(7) DEFAULT NULL,\n" + \
            "  `title` char(15) DEFAULT NULL,\n" +  \
            "  `category` char(11) DEFAULT NULL,\n" +  \
            "  `abstract` char(30) DEFAULT NULL,\n" +  \
            "  `articleTags` char(14) DEFAULT NULL,\n" +  \
            "  `authors` char(13) DEFAULT NULL,\n" +  \
            "  `language` char(3) DEFAULT NULL,\n" +  \
            "  `text` char(31) DEFAULT NULL,\n" +  \
            "  `image` char(64) DEFAULT NULL,\n" +  \
            "  `video` char(64) DEFAULT NULL\n) ENGINE=InnoDB DEFAULT CHARSET=utf8;\n\n")
    file.write("LOCK TABLES `article` WRITE;\n")
    
    file.write('INSERT INTO `article` VALUES\n' + "".join(dbms1_rows) + ';')

# # Write the dbms2 SQL file
# with open('article_dbms2.sql', 'w') as file:
#     file.write("DROP TABLE IF EXISTS `article`;\n")
#     file.write("CREATE TABLE `article` (\n" + \
#             "  `timestamp` char(14) DEFAULT NULL,\n" + \
#             "  `id` char(7) DEFAULT NULL,\n" + \
#             "  `aid` char(7) DEFAULT NULL,\n" + \
#             "  `title` char(15) DEFAULT NULL,\n" +  \
#             "  `category` char(11) DEFAULT NULL,\n" +  \
#             "  `abstract` char(30) DEFAULT NULL,\n" +  \
#             "  `articleTags` char(14) DEFAULT NULL,\n" +  \
#             "  `authors` char(13) DEFAULT NULL,\n" +  \
#             "  `language` char(3) DEFAULT NULL,\n" +  \
#             "  `text` char(31) DEFAULT NULL,\n" +  \
#             "  `image` char(64) DEFAULT NULL,\n" +  \
#             "  `video` char(64) DEFAULT NULL\n) ENGINE=InnoDB DEFAULT CHARSET=utf8;\n\n")
#     file.write("LOCK TABLES `article` WRITE;\n")
#     file.write('INSERT INTO `article` VALUES\n' + ''.join(dbms2_rows) + ';')
