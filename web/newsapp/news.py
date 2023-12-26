from flask import Blueprint, url_for, request, render_template, send_from_directory
import pymysql
from datetime import datetime
import math

bp = Blueprint('index', __name__,)


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
    total_article = 1000
    articles = get_article(page, 4)
    
    total_pages = math.ceil(total_article / 4)
    return render_template('index.html', articles=articles, total_pages = total_pages, current_page=page)

def get_article(page, per_page):

      # cursor2.execute("SELECT aid, readNum, commentNum FROM be_read LIMIT %s OFFSET %s", (page, per_page))
      cursor1.execute("SELECT aid, readNum, commentNum FROM be_read LIMIT %s OFFSET %s", (per_page, page))
      data1 = cursor1.fetchall()
      print(data1[0])
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
            publishdatae = datetime.utcfromtimestamp(publishTime)
            article['id'] = art_info[1]
            article["publishTime"] = publishdatae
            article["title"] = art_info[3]
            article['content'] = get_article_content(aid)
            article["category"] = art_info[4]
            article["abstract"] = art_info[5]
            article["tags"] = art_info[6]   
            article["author"] = art_info[7]
            article['lang'] = art_info[8]
            article['text'] = art_info[9]
            article['image'] = media_paths(aid, art_info[10])
            article['video'] = media_paths(aid, art_info[11])
            #  print(type(article))
            articles.append(article)
         
      return articles

def get_article_content(aid):
   base_path = "D:/THU/semester1/DDBS/Project/db-generation/articles"
   with open(f"{base_path}/article{aid}/text_a{aid}.txt") as f:
      return f.read()


@bp.route('/article/<int:aid>')
def article(aid):
   article_data = {}
   cursor1.execute("SELECT aid, readNum, commentNum FROM be_read WHERE aid = %s", (aid))
   be_read = cursor1.fetchone()
   cursor1.execute("SELECT * FROM article WHERE aid = %s", (aid))
   article = cursor1.fetchone()
   if not article:
      cursor2.execute("SELECT * FROM article WHERE aid = %s", (aid))
      article = cursor2.fetchone()
   article_data["readNum"] = be_read[1]
   article_data["commentNum"] = be_read[2]
   article_data["aid"] = be_read[0]
   publishTime = int(article[0])/1000
   publishdate = datetime.utcfromtimestamp(publishTime)
   article_data['publishTime'] = publishdate
   article_data['content'] = get_article_content(aid)
   article_data['title'] = article[3]
   article_data['category'] = article[4]
   article_data['abstract'] = article[5]
   article_data['tags'] = article[6]
   article_data['author'] = article[7]
   article_data['lang'] = article[8]
   article_data['image'] = media_paths(aid, article[10])
   article_data['video'] = media_paths(aid, article[11])
   
   return render_template('article.html', article = article_data)

def media_paths(aid, image_name):
   names = image_name.split(",")
   paths = []
   # base_path = "D:/THU/semester1/DDBS/Project/db-generation/articles"
   for name in names:
      name.strip()
      if name:
         paths.append(f"/article{aid}/{name}")
   print(paths)
   return paths

@bp.route('/media/<path:filename>')
def custom_static(filename):
    return send_from_directory(r'D:/THU/semester1/DDBS/Project/db-generation/articles', filename)