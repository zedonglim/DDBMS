import pymysql

# Connect to your MySQL database
connection = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='TAN@mysql',
    database='ddbms_orig',
    port=3306
)

# Create a cursor object to execute SQL queries
cursor = connection.cursor()

# Query the user, article, and read tables
cursor.execute("SELECT * FROM user;")
users = cursor.fetchall()

cursor.execute("SELECT * FROM article;")
articles = cursor.fetchall()

cursor.execute("SELECT * FROM user_read;")
reads = cursor.fetchall()

# Close the database connection
connection.close()

# Now you can use the fetched data to generate the "Be Read" table
with open("be_read/be_read.sql", "w+") as f:
    f.write("DROP TABLE IF EXISTS `be_read`;\n")
    f.write("CREATE TABLE `be_read` (\n" + \
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
            "  PRIMARY KEY (`id`)\n" + \
            ") ENGINE=InnoDB DEFAULT CHARSET=utf8;\n\n")

    f.write("LOCK TABLES `be_read` WRITE;\n")
    
    # Dictionary to keep track of read, comment, agree, and share counts 
    read_count = {}
    comment_count = {}
    agree_count = {}
    share_count = {}

    # Dictionary to store lists of uids for read, comment, agree, share, and timestamp of each aid
    read_uid_lists = {}
    comment_uid_lists = {}
    agree_uid_lists = {}
    share_uid_lists = {}
    aid_timestamp_lists = {}

    # Set to store distinct aid values from user_read table
    distinct_aids = set()

    # Iterate over the read data to populate counts and collect distinct aids
    for read in reads:
        aid = read[3]  # Assuming the column index for 'aid' in user_read table is 3
        uid = read[2]  # Assuming the column index for 'uid' in user_read table is 2
        timestamp = read[0] # Assuming the column index for 'timestamp' in user_read table is 1

        if aid not in distinct_aids:
            distinct_aids.add(aid)

        # Read counts
        read_count[aid] = read_count.get(aid, 0) + 1
        read_uid_lists.setdefault(aid, set()).add(uid)

        # Timestamp
        aid_timestamp_lists.setdefault(aid, set()).add(timestamp)

        # Comment counts
        if read[6] == "1":  # Assuming the column index for 'commentOrNot' in user_read table is 6
            comment_count.setdefault(aid, 0)
            comment_count[aid] += 1
            comment_uid_lists.setdefault(aid, set()).add(uid)

        # Agree counts
        if read[5] == "1":  # Assuming the column index for 'agreeOrNot' in user_read table is 5
            agree_count.setdefault(aid, 0)
            agree_count[aid] += 1
            agree_uid_lists.setdefault(aid, set()).add(uid)

        # Share counts
        if read[7] == "1":  # Assuming the column index for 'shareOrNot' in user_read table is 7
            share_count.setdefault(aid, 0)
            share_count[aid] += 1
            share_uid_lists.setdefault(aid, set()).add(uid)

    # Iterate over the distinct aids to generate the "Be Read" table entries
    f.write("INSERT INTO `be_read` (`timestamp`, `aid`, `readNum`, `readUidList`, `commentNum`, `commentUidList`, `agreeNum`, `agreeUidList`, `shareNum`, `shareUidList`) VALUES\n")
    for index, aid in enumerate(distinct_aids):
        read_num = read_count.get(aid, 0)
        read_uid_list = ",".join(map(str, read_uid_lists.get(aid, [])))

        comment_num = comment_count.get(aid, 0)
        comment_uid_list = ",".join(map(str, comment_uid_lists.get(aid, [])))

        agree_num = agree_count.get(aid, 0)
        agree_uid_list = ",".join(map(str, agree_uid_lists.get(aid, [])))

        share_num = share_count.get(aid, 0)
        share_uid_list = ",".join(map(str, share_uid_lists.get(aid, [])))

        timestamp_list = ",".join(map(str, aid_timestamp_lists.get(aid, [])))

        f.write("(" + \
                "\"" + timestamp_list + "\", " + \
                "\"" + aid + "\", " + \
                str(read_num) + ", " + \
                "\"" + read_uid_list + "\", " + \
                str(comment_num) + ", " + \
                "\"" + comment_uid_list + "\", " + \
                str(agree_num) + ", " + \
                "\"" + agree_uid_list + "\", " + \
                str(share_num) + ", " + \
                "\"" + share_uid_list + "\"" + ")" + ("," if index < len(distinct_aids) - 1 else ";") + "\n")

    f.write("UNLOCK TABLES;\n\n\n")
