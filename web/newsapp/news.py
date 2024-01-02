from flask import Blueprint, url_for, request, render_template, send_from_directory, Response
import pymysql
from datetime import datetime
import math
import mimetypes
from minio import Minio


bp = Blueprint('index', __name__,)


minio_client = Minio('127.0.0.1:9000',
                     access_key='minioadmin',
                     secret_key='minioadmin',
                     secure=False)


def get_db(dbms):
   connection = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='TAN@mysql',
    database=dbms,
    port=3306
    )
   return connection

dbms1_conn = get_db("dmbs1")
dmbs2_conn = get_db("dmbs2")

cursor1 = dbms1_conn.cursor()
cursor2 = dmbs2_conn.cursor()
      
@bp.route('/')
def index():
   # datafrom dmbs1
    page = request.args.get('page', 1, type=int)
    total_article = get_article_num()
    articles = get_article(page, 4)
    popular = popular_article()
    
    total_pages = math.ceil(total_article / 4)
    return render_template('index.html', articles=articles, total_pages = total_pages, current_page=page, popular=popular)
def get_article_num():
    cursor2.execute("SELECT COUNT(*) FROM article")
    total_article = cursor2.fetchone()[0]
    
    return total_article

def get_article(page, per_page):
      per_page = per_page//2
      cursor2.execute("SELECT aid, readNum, commentNum FROM be_read LIMIT %s OFFSET %s", (per_page, page))
      cursor1.execute("SELECT aid, readNum, commentNum FROM be_read LIMIT %s OFFSET %s", (per_page, page))
      data1 = cursor1.fetchall()
      data2 = cursor2.fetchall()
      articles = []
      for row in data1: 
            article = {}
            aid = row[0]
            article["aid"] = aid
            article["readNum"] = row[1]
            article["commentNum"] = row[2]
            cursor1.execute("SELECT * FROM article WHERE aid = %s", (aid))
            art_info = cursor1.fetchone()
            if not art_info:
               cursor2.execute("SELECT * FROM article WHERE aid = %s", (aid))
               art_info = cursor2.fetchone()
               
            publishTime = int(art_info[0])/1000
            publishdatae = datetime.utcfromtimestamp(publishTime).strftime('%Y-%m-%d %H:%M')
            article['id'] = art_info[1]
            article["publishTime"] = publishdatae
            article["title"] = get_article_title(aid)
            article['content'] = get_article_content(aid)
            article["category"] = art_info[4]
            article["abstract"] = get_article_abstract(aid)
            article["tags"] = art_info[6]   
            article["author"] = art_info[7]
            article['lang'] = art_info[8]
            article['text'] = art_info[9]
            article['image'] = media_paths(aid, art_info[10])
            article['video'] = media_paths(aid, art_info[11])
        
            #  print(type(article))
            articles.append(article)
      for row in data2:
        article = {}
        aid = row[0]
        article["aid"] = aid
        article["readNum"] = row[1]
        article["commentNum"] = row[2]
        cursor2.execute("SELECT * FROM article WHERE aid = %s", (aid))
        art_info = cursor2.fetchone()
        if not art_info:
            cursor1.execute("SELECT * FROM article WHERE aid = %s", (aid))
            art_info = cursor1.fetchone()
            
        publishTime = int(art_info[0])/1000
        publishdatae = datetime.utcfromtimestamp(publishTime)
        article['id'] = art_info[1]
        article["publishTime"] = publishdatae
        article["title"] = get_article_title(aid)
        article['content'] = get_article_content(aid)
        article["category"] = art_info[4]
        article["abstract"] = get_article_abstract(aid)
        article["tags"] = art_info[6]   
        article["author"] = art_info[7]
        article['lang'] = art_info[8]
        article['text'] = art_info[9]
        article['image'] = media_paths(aid, art_info[10])
        article['video'] = media_paths(aid, art_info[11])
        #  print(type(article))
        articles.append(article)
      return articles
  
def popular_article():
    popular_articles = {}
    cursor1.execute("SELECT articleAidList FROM popular_rank")
    daily_ids = cursor1.fetchall()
    daily_ids = tuple(daily_ids[0][0].split(","))
    # print("Daily ids:", daily_ids)
    cursor1.execute(f"SELECT aid, readNum FROM be_read WHERE aid IN {daily_ids} ORDER BY readNum DESC LIMIT 5")
    daily_popular = cursor1.fetchall()
    if not daily_popular:
        cursor2.execute(f"SELECT aid, readNum FROM be_read WHERE aid IN {daily_ids} ORDER BY readNum DESC LIMIT 5")
        daily_popular = cursor2.fetchall()
    daily_popular_articles = []
    for row in daily_popular:
        daily = {}
        aid = row[0]
        # cursor1.execute("SELECT * FROM article WHERE aid = %s", (aid))
        # art_info = cursor1.fetchone()
        # if not art_info:
        #     cursor2.execute("SELECT * FROM article WHERE aid = %s", (aid))
        #     art_info = cursor2.fetchone()
        daily['aid'] = aid
        daily["title"] = get_article_title(aid)
        daily_popular_articles.append(daily)
    popular_articles["daily"] = daily_popular_articles
    
    
    cursor2.execute("SELECT articleAidList FROM popular_rank WHERE temporalGranularity = 'weekly'")
    weekly_ids = cursor2.fetchall()
    weekly_ids = tuple(weekly_ids[0][0].split(","))
    cursor2.execute(f"SELECT aid, readNum FROM be_read WHERE aid IN {weekly_ids} ORDER BY readNum DESC LIMIT 5")
    weekly_popular = cursor2.fetchall()
    if not weekly_popular:
        cursor1.execute(f"SELECT aid, readNum FROM be_read WHERE aid IN {weekly_ids} ORDER BY readNum DESC LIMIT 5")
        weekly_popular = cursor1.fetchall()
    weekely_popular_articles = []
    
    for row in weekly_popular:
        weekly = {}
        aid = row[0]
        # cursor2.execute("SELECT * FROM article WHERE aid = %s", (aid))
        # art_info = cursor2.fetchone()
        # if not art_info:
        #     cursor1.execute("SELECT * FROM article WHERE aid = %s", (aid))
        #     art_info = cursor2.fetchone()
        weekly['aid'] = aid
        weekly["title"] = get_article_title(aid)
        weekely_popular_articles.append(weekly)
    
    popular_articles["weekly"] = weekely_popular_articles
        
        
    cursor2.execute("SELECT articleAidList FROM popular_rank WHERE temporalGranularity = 'monthly'")
    monthly_ids = cursor2.fetchall()
    monthly_ids = tuple(monthly_ids[0][0].split(","))
    cursor2.execute(f"SELECT aid, readNum FROM be_read WHERE aid IN {monthly_ids} ORDER BY readNum DESC LIMIT 5")
    monthly_popular = cursor2.fetchall()
    if not monthly_popular:
        cursor1.execute(f"SELECT aid, readNum FROM be_read WHERE aid IN {monthly_ids} ORDER BY readNum DESC LIMIT 5")
        monthly_popular = cursor1.fetchall()
    monthly_popular_articles = []
    for row in monthly_popular:
        monthly = {}
        aid = row[0]
        # cursor2.execute("SELECT * FROM article WHERE aid = %s", (aid))
        # art_info = cursor2.fetchone()
        # if not art_info:
        #     cursor1.execute("SELECT * FROM article WHERE aid = %s", (aid))
        #     art_info = cursor2.fetchone()
        monthly['aid'] = aid
        monthly["title"] = get_article_title(aid)
        monthly_popular_articles.append(monthly)
        
    popular_articles["monthly"] = monthly_popular_articles
    # print(type(popular_articles))
    # print(type(popular_articles["daily"]))
    
    # print(popular_articles)
    return popular_articles
    
def get_article_content(aid):
    try:
        data = minio_client.get_object('articledata', f'articles/article{aid}/text_a{aid}.txt')
        return data.read().decode('utf-8')
    except Exception as e:
        print(e)
        return None

def get_article_title(aid):
    try:
        data = minio_client.get_object('articledata', f'articles/article{aid}/text_a{aid}.txt')
        return data.read().decode('utf-8').split('\n')[0]
    except Exception as e:
        print(e)
        return None
    
def get_article_abstract(aid):
    try:
        data = minio_client.get_object('articledata', f'articles/article{aid}/text_a{aid}.txt')
        content = data.read().decode('utf-8')
        lines = content.split('\n')
        return lines[2]
    except Exception as e:
        print(e)
        return None
    
@bp.route('/article/<int:aid>')
def article(aid):
   article_data = {}
   cursor1.execute("SELECT aid, readNum, commentNum FROM be_read WHERE aid = %s", (aid))

   be_read = cursor1.fetchone()
   if not be_read:
       cursor2.execute("SELECT aid, readNum, commentNum FROM be_read WHERE aid = %s", (aid))
       be_read = cursor2.fetchone()
#    print("\nBe read 1: ", be_read)
   cursor1.execute("SELECT * FROM article WHERE aid = %s", (aid))
   article = cursor1.fetchone()
   if not article:
      cursor2.execute("SELECT * FROM article WHERE aid = %s", (aid))
      article = cursor2.fetchone()
   article_data["readNum"] = be_read[1]
   article_data["commentNum"] = be_read[2]
   article_data["aid"] = be_read[0]
   publishTime = int(article[0])/1000
   publishdate = datetime.utcfromtimestamp(publishTime).strftime('%Y-%m-%d %H:%M')
   article_data['publishTime'] = publishdate
   article_data['content'] = get_article_content(aid)
   article_data['title'] = get_article_title(aid)
   article_data['category'] = article[4]
   article_data['abstract'] = get_article_abstract(aid)
   article_data['tags'] = article[6]
   article_data['author'] = article[7]
   article_data['lang'] = article[8]
   article_data['image'] = media_paths(aid, article[10])
   article_data['video'] = media_paths(aid, article[11])
   
   popular = popular_article()
   return render_template('article.html', article = article_data, popular=popular)


def media_paths(aid, media_names):
    # print("Media names:", media_names)
    names = media_names.split(",")
    paths = []
    for name in names:
        name = name.strip()
        if name:
            paths.append(url_for('index.custom_static', filename=f'article{aid}/{name}'))
    # print("Paths:", paths)
    return paths


@bp.route('/<path:filename>')
def custom_static(filename):
    try:
        # Prepend the base path to the filename
        full_path = 'articles/' + filename

        # Fetch the object from MinIO using the full path
        data = minio_client.get_object('articledata', full_path)
        content_type = mimetypes.guess_type(full_path)[0] or 'application/octet-stream'

        # Stream the data back in the response
        return Response(data.stream(32*1024), content_type=content_type)
    except Exception as e:
        print(e)  # Log the error for debugging
        return str(e), 404
def get_article_num_by_category(category):
    cursor2.execute("SELECT COUNT(*) FROM article WHERE category = %s", (category))
    total_article = cursor2.fetchone()[0]
    return total_article

@bp.route('/<string:category>')    
def filter_category(category):
    total_article = get_article_num_by_category(category)
    page = request.args.get('page', 1, type=int)
    per_page = 10
    total_pages = math.ceil(total_article / per_page)
    
    cursor2.execute("SELECT br.aid, br.readNum, br.commentNum FROM be_read br INNER JOIN article a on a.aid = br.aid WHERE a.category = %s LIMIT %s OFFSET %s", (category, per_page, page))
    
    data2 = cursor2.fetchall()
    articles = []
    popular = popular_article()
    for row in data2:
        article = {}
        aid = row[0]
        article["aid"] = aid
        article["readNum"] = row[1]
        article["commentNum"] = row[2]
        cursor2.execute("SELECT * FROM article WHERE aid = %s", (aid))
        art_info = cursor2.fetchone()
        if not art_info:
            cursor1.execute("SELECT * FROM article WHERE aid = %s", (aid))
            art_info = cursor1.fetchone()
            
        publishTime = int(art_info[0])/1000
        publishdatae = datetime.utcfromtimestamp(publishTime)
        article['id'] = art_info[1]
        article["publishTime"] = publishdatae
        article["title"] = get_article_title(aid)
        article['content'] = get_article_content(aid)
        article["category"] = art_info[4]
        article["abstract"] = get_article_abstract(aid)
        article["tags"] = art_info[6]   
        article["author"] = art_info[7]
        article['lang'] = art_info[8]
        article['text'] = art_info[9]
        article['image'] = media_paths(aid, art_info[10])
        article['video'] = media_paths(aid, art_info[11])
        #  print(type(article))
        articles.append(article)
    return render_template('index.html', articles=articles, total_pages = total_pages, current_page=page, popular=popular)

@bp.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == "POST":
        uid = request.form.get('uid')
        print(uid)
        print(type(uid))
    else:
        uid = 1837
    page = request.args.get('page', 1, type=int)
    total_read = get_user_read_num()
    # articles = get_article(page, 4)
    popular = popular_article()
    per_page = 10
    
    total_pages = math.ceil(total_read / per_page)

    users = get_users(uid)
    
    return render_template('users.html', users=users, total_pages = total_pages, current_page=page, popular=popular)

def get_users(uid):
    users = []
    cursor1.execute("SELECT u.uid, u.name, u.region, ur.aid, ur.readTimeLength FROM user u INNER JOIN user_read ur on u.uid = ur.uid where u.uid=%s", (uid))
    users1 = cursor1.fetchall()
    if not users1:
         cursor2.execute("SELECT u.uid, u.name, u.region, ur.aid, ur.readTimeLength FROM user u INNER JOIN user_read ur on u.uid = ur.uid where u.uid=%s", (uid))
         users1 = cursor2.fetchall()
         if not users1:
            return []
    for row in users1:
        user = {}
        user['uid'] = row[0]
        user['name'] = row[1]
        user['region'] = row[2]
        user['aid'] = row[3]
        user['readTimeLength'] = row[4]
        users.append(user)
   
    
    # users2 = cursor2.fetchall()
    # for row in users2:
    #     user = {}
    #     user['uid'] = row[0]
    #     user['name'] = row[1]
    #     user['region'] = row[2]
    #     user['aid'] = row[3]
    #     user['readTimeLength'] = row[4]
    #     users.append(user)
    
    return users


def get_user_read_num():
    cursor1.execute("SELECT count(*) FROM user_read")
    count1 = cursor1.fetchone()[0]
    cursor2.execute("SELECT count(*) FROM user_read")
    count2 = cursor2.fetchone()[0]
    return count1 + count2