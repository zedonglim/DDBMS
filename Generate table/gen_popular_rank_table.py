import pymysql
from datetime import datetime

# Connect to your MySQL database
connection = pymysql.connect(
    host='your_host',
    user='your_user',
    password='your_password',
    database='your_database',
    port='your_port'
)

# Create a cursor object to execute SQL queries
cursor = connection.cursor()

# Query the be-read table
cursor.execute("SELECT * FROM be_read ORDER BY readNum DESC LIMIT 10;")
top_reads = cursor.fetchall()

# Close the database connection
connection.close()

# Classify articles into daily, weekly, and monthly
daily_articles = []
weekly_articles = []
monthly_articles = []

current_date = datetime.now()

for read in top_reads:
    read_timestamp = datetime.utcfromtimestamp(read[1])
    time_difference = current_date - read_timestamp

    if time_difference.days <= 1:
        daily_articles.append(read[2])  # Assuming aid is at index 2, adjust accordingly
    elif time_difference.days <= 7:
        weekly_articles.append(read[2])
    elif time_difference.days <= 30:
        monthly_articles.append(read[2])

# Convert current_date to Unix timestamp
current_unix_timestamp = int(current_date.timestamp())

# Now you can use the fetched data to generate the "Popular Rank" table
with open("popular_rank.sql", "w+") as f:
    f.write("DROP TABLE IF EXISTS `popular_rank`;\n")
    f.write("CREATE TABLE `popular_rank` (\n" + \
            "  `id` bigint NOT NULL AUTO_INCREMENT,\n" + \
            "  `timestamp` char(14) DEFAULT NULL,\n" + \
            "  `temporalGranularity` text,\n" +  \
            "  `articleAidList` text,\n" + \
            "  PRIMARY KEY (`id`),\n" + \
            ") ENGINE=InnoDB DEFAULT CHARSET=utf8;\n\n")

    f.write("LOCK TABLES `popular_rank` WRITE;\n")

    # Prepare the data for insertion
    data = [
        (str(current_unix_timestamp), 'daily', ','.join(map(str, daily_articles))),
        (str(current_unix_timestamp), 'weekly', ','.join(map(str, weekly_articles))),
        (str(current_unix_timestamp), 'monthly', ','.join(map(str, monthly_articles)))
    ]

    # Insert data into the popular_rank table
    f.write("INSERT INTO `popular_rank` (`timestamp`, `temporalGranularity`, `articleAidList`) VALUES\n")
    for i, (timestamp, granularity, article_list) in enumerate(data):
        f.write(f"({timestamp}, '{granularity}', '{article_list}')")
        if i < len(data) - 1:
            f.write(",\n")
        else:
            f.write(";\n")
    # Unlock the tables
    f.write("UNLOCK TABLES;\n")
