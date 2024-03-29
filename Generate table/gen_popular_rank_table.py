import pymysql
from datetime import datetime, timedelta

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
    read_smallest_timestamp = datetime.utcfromtimestamp(min(timestamps))

    next_day = read_smallest_timestamp + timedelta(days=1)
    next_week = read_smallest_timestamp + timedelta(days=7)
    next_month = read_smallest_timestamp + timedelta(days=30)

    # Initialize counters for each temporal granularity
    daily_count = 0
    weekly_count = 0
    monthly_count = 0

    # Iterate through timestamps and count occurrences within ranges
    for timestamp in timestamps:

        # Check if the timestamp falls within the specified ranges
        if read_smallest_timestamp <= datetime.utcfromtimestamp(timestamp) <= next_day:
            daily_count += 1
        if read_smallest_timestamp <= datetime.utcfromtimestamp(timestamp) <= next_week:
            weekly_count += 1
        if read_smallest_timestamp <= datetime.utcfromtimestamp(timestamp) <= next_month:
            monthly_count += 1

    # Determine the temporal granularity based on the threshold values
    threshold_daily = 4
    threshold_weekly = 12
    threshold_monthly = 35
    
    temporal_granularity = ""
    if daily_count >= threshold_daily:
        temporal_granularity = "daily"
    if weekly_count >= threshold_weekly:
        temporal_granularity = "weekly"
    if monthly_count >= threshold_monthly:
        temporal_granularity = "monthly"

    # Add the article ID to the corresponding list based on the determined granularity
    if temporal_granularity == "daily":
        daily_articles.append(read[2])
    elif temporal_granularity == "weekly":
        weekly_articles.append(read[2])
    elif temporal_granularity == "monthly":
        monthly_articles.append(read[2])

# Convert current_date to Unix timestamp
current_date = datetime.now()
current_unix_timestamp = int(current_date.timestamp())*1000

# Now you can use the fetched data to generate the "Popular Rank" table
with open("popular_rank.sql", "w+") as f:
    f.write("DROP TABLE IF EXISTS `popular_rank`;\n")
    f.write("CREATE TABLE `popular_rank` (\n" + \
            "  `id` bigint NOT NULL AUTO_INCREMENT,\n" + \
            "  `timestamp` char(14) DEFAULT NULL,\n" + \
            "  `temporalGranularity` text,\n" +  \
            "  `articleAidList` text,\n" + \
            "  PRIMARY KEY (`id`)\n" + \
            ") ENGINE=InnoDB DEFAULT CHARSET=utf8;\n\n")

    f.write("LOCK TABLES `popular_rank` WRITE;\n")
    print(f"Daily: {len(daily_articles)}\nWeekly: {len(weekly_articles)}\nMonthly: {len(monthly_articles)}\n")
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