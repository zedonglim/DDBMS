# DDBMS
Distributed Database Management System for THUACP2023

## When running a large script in mysql workbence
### SET GLOBAL max_allowed_packet=1000000

```
SELECT * FROM dmbs1.user 
WHERE find_in_set(uid, (SELECT readUidList FROM dmbs1.be_read  WHERE aid=9));
```
#### from gpt

```
from datetime import datetime, timedelta
from collections import defaultdict

# Example data: a dictionary where keys are article IDs and values are lists of interaction timestamps
articles = {
    'article_1': [timestamp1, timestamp2, ...],
    'article_2': [timestamp3, timestamp4, ...],
    # ...
}

# Define popularity criteria
daily_threshold = 100   # example threshold for daily popularity
weekly_threshold = 500  # example threshold for weekly popularity
monthly_threshold = 2000 # example threshold for monthly popularity

# Function to convert timestamps to datetime
def convert_to_datetime(timestamps):
    return [datetime.fromtimestamp(ts / 1000) for ts in timestamps]

# Function to classify articles
def classify_articles(articles):
    popularity = defaultdict(lambda: {"daily": False, "weekly": False, "monthly": False})

    for article_id, timestamps in articles.items():
        timestamps = convert_to_datetime(timestamps)

        # Count interactions per day, week, and month
        daily_counts = defaultdict(int)
        weekly_counts = defaultdict(int)
        monthly_counts = defaultdict(int)

        for ts in timestamps:
            daily_counts[ts.date()] += 1
            weekly_counts[ts.isocalendar()[0:2]] += 1  # (year, week number)
            monthly_counts[(ts.year, ts.month)] += 1

        # Check if counts meet thresholds
        if any(count >= daily_threshold for count in daily_counts.values()):
            popularity[article_id]["daily"] = True
        if any(count >= weekly_threshold for count in weekly_counts.values()):
            popularity[article_id]["weekly"] = True
        if any(count >= monthly_threshold for count in monthly_counts.values()):
            popularity[article_id]["monthly"] = True

    return popularity

# Classify articles
popularity_classification = classify_articles(articles)

```