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
    file.write('INSERT INTO `user` VALUES\n' + "".join(dbms1_rows) + ';')

# Write the dbms2 SQL file
with open('user_dbms2.sql', 'w') as file:
    file.write('INSERT INTO `user` VALUES\n' + ''.join(dbms2_rows) + ';')