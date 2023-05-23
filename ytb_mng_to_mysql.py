import pandas as pd
from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017")
mydb = client["Youtube"]
ytchnl1 = mydb["youtubechannel1"]
#Query = { Channel_Name : { Channel_Id : "UCgBncpylJ1kiVaPyP-PZauQ" } }
limit = 1000000
num_documents = mydb.ytchnl1.count_documents({})
#documents = mydb.ytchnl.find(Query, limit=limit)
#for document in documents:
#    print(document)
#client.close()
print(num_documents)

documents = mydb.ytchnl1.find()
channel_info = {'channel_id': [], 'channel_name': [], 'channel_type': [], 'channel_views': [], 'channel_description': [], 'channel_status': []}
playlist_info = {'channel_id': [], 'playlist_name': [], 'playlist_id': []}
comment_info = {'comment_id': [], 'video_id': [], 'comment_text': [], 'comment_author': [], 'comment_published_date': []}
video_info = {'video_name': [], 'video_id': [], 'playlist_id': [], 'video_description': [], 'published_date': [], 'view_count': [], 'like_count': [], 'dislike_count': [], 'favorite_count': [], 'comment_count': [], 'duration': [], 'thumbnail': [], 'caption_status': []}
docid = []
chnname = []
for document in documents:
    #print(document["_id"])
    docid.append(document["_id"])
    i = document["Channel_Name"]["Channel_Name"]
    j = document["Channel_Name"]["Channel_Id"]
    k = document["Channel_Name"]["Subscription_Count"]
    l = document["Channel_Name"]["Channel_Views"]
    m = document["Channel_Name"]["Channel_Description"]
    n = document["Channel_Name"]["Playlist_Id"]
    o = document["Channel_Name"]["playlist_Title"]
    p = "NAN"
    channel_info['channel_id'].append(j)
    channel_info['channel_name'].append(i)
    channel_info['channel_type'].append(p)
    channel_info['channel_views'].append(l)
    channel_info['channel_description'].append(m)
    channel_info['channel_status'].append(p)
    playlist_info['channel_id'].append(j)
    playlist_info['playlist_name'].append(o)
    playlist_info['playlist_id'].append(n)
    for x in document:
        if x == "Channel_Name":
            continue
        elif x == "_id":
            continue
        else:
            #print("video_id:",x)
            #print(type(i))
            r = document[x]["Video_Id"]
            s = document[x]["Video_Name"]
            t = document[x]["Video_Description"]
            u = document[x]["View_Count"]
            v = document[x]["PublishedAt"]
            w = document[x]["Like_Count"]
            a = document[x]["Favorite_Count"]
            b = document[x]["Comment_Count"]
            c = document[x]["Duration"]
            d = document[x]["Thumbnail"]
            e = document[x]["Caption_Status"]
            video_info['playlist_id'].append(n)
            video_info['video_id'].append(r)
            video_info['video_name'].append(s)
            video_info['video_description'].append(t)
            video_info['published_date'].append(v)
            video_info['view_count'].append(u)
            video_info['like_count'].append(w)
            video_info['dislike_count'].append(p)
            video_info['favorite_count'].append(a)
            video_info['comment_count'].append(b)
            video_info['duration'].append(c)
            video_info['thumbnail'].append(d)
            video_info['caption_status'].append(e)
        for y in document[x]:
            if "Comment_Id" in y:
                f = document[x][y]['comment']["comment_id"]
                g = document[x][y]['comment']["comment_text"]
                h = document[x][y]['comment']["comment_author"]
                ia = document[x][y]['comment']["comment_publishedate"]
                comment_info['comment_id'].append(f)
                comment_info['video_id'].append(r)
                comment_info['comment_text'].append(g)
                comment_info['comment_author'].append(h)
                comment_info['comment_published_date'].append(ia)
            #print(type(y))
        #print(video_info)

channel_df = pd.DataFrame(channel_info)
playlist_df = pd.DataFrame(playlist_info)
video_df = pd.DataFrame(video_info)
comment_df = pd.DataFrame(comment_info)
#print(docid)
print(channel_df)
print(playlist_df)
print(video_df)
print(comment_df)
video_df['dislike_count'] = video_df['dislike_count'].replace(['NAN'],'0')
video_df['published_date'] =  pd.to_datetime(video_df['published_date'], infer_datetime_format=True)
video_df['dislike_count'] = video_df['dislike_count'].astype(int)
video_df['duration'] = video_df['duration'].str.replace('PT', '')
video_df['duration'] = pd.to_timedelta(video_df['duration']).dt.total_seconds().astype(int)
video_df['duration'] = video_df['duration']/3600

video_df.drop_duplicates(subset=['video_id'], keep='first', inplace = True)
channel_df.drop_duplicates(subset=['channel_id'], keep='first', inplace = True)
playlist_df.drop_duplicates(subset=['playlist_id'], keep='first', inplace = True)
comment_df.drop_duplicates(subset=['comment_id'], keep='first', inplace = True)

video_df['like_count']=video_df.like_count.replace('Not Available', '0')
video_df['like_count'] = video_df['like_count'].astype(int)

comment_df['comment_published_date'] = pd.to_datetime(comment_df['comment_published_date'], infer_datetime_format=True)

from sqlalchemy import create_engine

engine1 = create_engine("mysql+pymysql://{user}:{pw}@localhost".format(user="root", pw="root123"))

existing_databases = engine1.execute("SHOW DATABASES;")
print(existing_databases)
# Results are a list of single item tuples, so unpack each tuple
existing_databases = [d[0] for d in existing_databases]
database = "youtubescrp1"
print(existing_databases)

if database not in existing_databases:
    engine1.execute("CREATE DATABASE {0}".format(database))
    print("Created database {0}".format(database))
    engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}".format(user="root", pw="root123", db = database))



    '''database = "Youtubescrp1"

    engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                       .format(user="root",
                               pw="root123",
                              db = database))'''
    #engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}".format(user="root", pw="root123", db = database))
    engine.execute("SET FOREIGN_KEY_CHECKS=0;")
    engine.execute("SET @@global.sql_mode= '';")
    engine.execute("create table Channel (channel_id VARCHAR(255) NOT NULL PRIMARY KEY, channel_name VARCHAR(255) NOT NULL, channel_type VARCHAR(255) NOT NULL, channel_views int(10) NOT NULL, channel_description VARCHAR(255) NOT NULL, channel_status VARCHAR(255));")
    engine.execute("create table Playlist (playlist_id VARCHAR(255) NOT NULL PRIMARY KEY, channel_id VARCHAR(255) NOT NULL, FOREIGN KEY(channel_id) REFERENCES Channel(channel_id), playlist_name VARCHAR(255) NOT NULL);")
    engine.execute("create table video (video_id VARCHAR(255) NOT NULL PRIMARY KEY, playlist_id VARCHAR(255) NOT NULL, FOREIGN KEY(playlist_id) REFERENCES Playlist(playlist_id), video_name VARCHAR(255) NOT NULL, video_description TEXT NOT NULL, published_date DATETIME, view_count int(10), like_count int(10), dislike_count int(10), favorite_count int(10), comment_count int(10), duration float(10), thumbnail VARCHAR(255), caption_status VARCHAR(255));")
    engine.execute("create table Comment (comment_id VARCHAR(255) NOT NULL PRIMARY KEY, video_id VARCHAR(255) NOT NULL, FOREIGN KEY(video_id) REFERENCES Video(video_id), comment_text TEXT , comment_author VARCHAR(255) NOT NULL, comment_published_date DATETIME NOT NULL, channel_description VARCHAR(255) NOT NULL, channel_status VARCHAR(255));")

    channel_df.to_sql('channel', con = engine, if_exists = 'append', index= False)
    playlist_df.to_sql('playlist', con = engine, if_exists = 'append', index= False)
    video_df.to_sql('video', con = engine, if_exists = 'append', index= False)
    comment_df.to_sql('comment', con = engine, if_exists = 'append', index= False)



    engine.execute("SET FOREIGN_KEY_CHECKS=1;")


    engine.execute("CREATE VIEW videos_Basic_info AS SELECT video_name, channel_name FROM video, channel, playlist WHERE video.playlist_id = playlist.playlist_id AND channel.channel_id = playlist.channel_id;")
    engine.execute("CREATE VIEW Least_Watched_videos AS select video_name, channel_name from video, channel, playlist WHERE video.playlist_id = playlist.playlist_id AND playlist.channel_id = channel.channel_id ORDER BY view_count LIMIT 10;")
    engine.execute("CREATE VIEW Top_videos AS select video_name, channel_name, view_count from video, channel, playlist WHERE video.playlist_id = playlist.playlist_id AND channel.channel_id = playlist.channel_id  ORDER BY view_count DESC LIMIT 10;")
    engine.execute("CREATE VIEW most_liked_videos AS select channel_name, video_name from video, channel, playlist WHERE video.playlist_id = playlist.playlist_id AND channel.channel_id = playlist.channel_id ORDER BY like_count DESC LIMIT 10;")
    engine.execute("CREATE VIEW Channel_that_published_video_in_year2022 AS SELECT channel_name FROM video, channel, playlist WHERE video.playlist_id = playlist.playlist_id AND channel.channel_id = playlist.channel_id AND YEAR(published_date)  = 2022;")
    engine.execute("CREATE VIEW More_comments AS select channel_name, comment_count, video_name from video, channel, playlist WHERE video.playlist_id = playlist.playlist_id AND channel.channel_id = playlist.channel_id ORDER BY comment_count DESC LIMIT 10;")
