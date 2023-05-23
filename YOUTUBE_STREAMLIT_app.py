import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
import subprocess
import sys

import os
cwd = os.getcwd()


st.title("Youtube Data Scrapping")

st.write("Please enter Channel Id with comma seperated")
ytb_channel_id = st.text_input("channel_ids")
button = st.button("Click to start harvesting")
if button:
    subprocess.run([f"{sys.executable}", cwd + "\\ytb_data_collection.py"])
    #subprocess.run([f"{sys.executable}", "C:\\Users\\kisho\\anaconda3\\ytb_data_collection.py"])
    #subprocess.run([f"{sys.executable}", "C:\\Users\\kisho\\anaconda3\\youtube_mongo_to_mysql.py"])

try:
    database = "Youtubescrp1"

    engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                           .format(user="root",
                                   pw="root123",
                                   db=database))

    df_sql_More_comments = pd.read_sql_query("Select * from more_comments;", con=engine)
    # df_sql_More_comments

    df_sql_Channel_that_published_video_in_year2022s = pd.read_sql_query(
        "SELECT * from channel_that_published_video_in_year2022;", con=engine)
    # df_sql_Channel_that_published_video_in_year2022s

    df_sql_most_liked_videos = pd.read_sql_query("SELECT * from most_liked_videos;", con=engine)
    # df_sql_most_liked_videos

    df_sql_channel = pd.read_sql_query("SELECT channel_views, channel_name from channel;", con=engine)
    # df_sql_channel

    df_sql_videos_basic_info = pd.read_sql_query("SELECT * from videos_Basic_info;", con=engine)
    # df_sql_videos_basic_info

    df_sql_Least_Watched_videos = pd.read_sql_query("SELECT * from least_Watched_videos;", con=engine)
    # df_sql_Least_Watched_videos

    df_sql_Top_videos = pd.read_sql_query("SELECT * from top_videos;", con=engine)
    # df_sql_Top_videos

    df_sql_video_comment_count = pd.read_sql_query("SELECT comment_count, video_name from video;", con=engine)
    # df_sql_video_comment_count
except BaseException as e:
    pass
st.sidebar.title("you tube data insights ")
button1 = st.sidebar.button("Click to proceed")
option = st.sidebar.selectbox('Search By', (
    'df_sql_More_comments', 'df_sql_Channel_that_published_video_in_year2022s', 'df_sql_most_liked_videos',
    'df_sql_channel', 'df_sql_videos_basic_info', 'df_sql_Least_Watched_videos', 'df_sql_Top_videos',
    'df_sql_video_comment_count'))
if button1:
    if option == 'df_sql_More_comments':
        st.write(df_sql_More_comments)
    elif option == 'df_sql_Channel_that_published_video_in_year2022s':
        st.write(df_sql_Channel_that_published_video_in_year2022s)
    elif option == 'df_sql_most_liked_videos':
        st.write(df_sql_most_liked_videos)
    elif option == 'df_sql_channel':
        st.write(df_sql_channel)
    elif option == 'df_sql_videos_basic_info':
        st.write(df_sql_videos_basic_info)
    elif option == 'df_sql_videos_basic_info':
        st.write(df_sql_videos_basic_info)
    elif option == 'df_sql_Least_Watched_videos':
        st.write(df_sql_Least_Watched_videos)
    elif option == 'df_sql_Top_videos':
        st.write(df_sql_Top_videos)
    elif option == 'df_sql_video_comment_count':
        st.write(df_sql_video_comment_count)

