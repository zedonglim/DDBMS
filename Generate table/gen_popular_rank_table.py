import pymysql
from datetime import datetime

# Connect to your MySQL database
connection = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='TAN@mysql',
    database='dmbs2',
    port=3306
)

# Create a cursor object to execute SQL queries
cursor = connection.cursor()

# Query the be-read table
cursor.execute("SELECT * FROM be_read;")
reads = cursor.fetchall()

# Close the database connection
connection.close()

# Classify articles into daily, weekly, and monthly
daily_articles = []
weekly_articles = []
monthly_articles = []

for read in reads:
    timestamps = [(int(timestamp) / 1000) for timestamp in read[1].split(",")]
    read_biggest_timestamp = datetime.utcfromtimestamp(max(timestamps))
    read_smallest_timestamp = datetime.utcfromtimestamp(min(timestamps))
    time_difference = read_biggest_timestamp - read_smallest_timestamp

    # Print the results
    print("Biggest Timestamp:", read_biggest_timestamp)
    print("Smallest Timestamp:", read_smallest_timestamp)
    print("Time Difference:", time_difference)

    if time_difference.days <= 1:
        daily_articles.append(read[2])  # Assuming aid is at index 2, adjust accordingly
    elif time_difference.days <= 7:
        weekly_articles.append(read[2])
    elif time_difference.days <= 30:
        monthly_articles.append(read[2])

# Convert current_date to Unix timestamp
current_date = datetime.now()
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
    f.write("UNLOCK TABLES;")