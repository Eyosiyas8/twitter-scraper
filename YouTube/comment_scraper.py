import os
from time import sleep
import requests
from googleapiclient.discovery import build
from pymongo import MongoClient
import sys
import datetime

import tqdm

# Initializing mongo db client
client = MongoClient('mongodb://localhost:27017/')
db = client['youtube-data']
collection = db['youtube']
# Set up the YouTube Data API v3 credentials
API_KEY = "AIzaSyCbGeJsInTEzEaW0Yib2MFi9Jn-lB4A46c"  # Replace with your own API key
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

basedir = os.path.dirname(os.path.abspath(__file__))
# Set up the YouTube Data API client
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)
link = os.path.join(basedir, 'url.txt')
# Input the YouTube video URL from the user 
try:
    osint_user_id = ''.join(sys.argv[2])
except:
    osint_user_id = 'Anonymous'


VIDEO_URL = ''.join(sys.argv[1])

# Extract the video ID from the YouTube video URL
video_id = VIDEO_URL.split("v=")[1]

# Request the video details using the YouTube Data API
video_response = youtube.videos().list(part="snippet, statistics", id=video_id).execute()
video_title = video_response["items"][0]["snippet"]["title"]
video_likes = video_response["items"][0]["statistics"]["likeCount"]
video_comments = video_response["items"][0]["statistics"]["commentCount"]

# Request the channel details using the YouTube Data API
channel_id = video_response["items"][0]["snippet"]["channelId"]
channel_response = youtube.channels().list(part="statistics", id=channel_id).execute()
channel_subscribers = channel_response["items"][0]["statistics"]["subscriberCount"]

# Try to retrieve the share count if available
video_shares = video_response["items"][0]["statistics"].get("shareCount", 0)

# Request the comments using the YouTube Data API
comments = []
next_page_token = None

while True:
    comment_threads = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        order="relevance",
        textFormat="plainText",
        maxResults=100,
        pageToken=next_page_token
    ).execute()

    for comment_thread in comment_threads["items"]:
        # Extract the top-level comment details
        top_level_comment = comment_thread["snippet"]["topLevelComment"]["snippet"]
        author_display_name = top_level_comment["authorDisplayName"]
        comment_text = top_level_comment["textDisplay"]
        comments.append((author_display_name, comment_text))

        # Check if there are any replies to the top-level comment
        if "replies" in comment_thread:
            replies = comment_thread["replies"]["comments"]
            for reply in replies:
                # Extract the reply details
                reply_author_display_name = reply["snippet"]["authorDisplayName"]
                reply_text = reply["snippet"]["textDisplay"]
                comments.append((reply_author_display_name, reply_text))

    if "nextPageToken" in comment_threads:
        next_page_token = comment_threads["nextPageToken"]
    else:
        break



    # Appending all the comments to one list
all_coments = []
for comment in comments:
    author_display_name, comment = comment
    all_coments.append({"username": author_display_name, "comment" :comment})


# Create a dictionary to store all the data
youtube_data = {
    "Timestamp": datetime.datetime.today(),
    "Video Title": video_title,
    "Link": VIDEO_URL,
    "Subscribers": channel_subscribers,
    # "Date of Post": video_published_date,
    "Comments Count": video_comments,
    "Likes": video_likes,
    "Shares": video_shares,
    "osint_user_id": osint_user_id,
    # "Subscriber Count": subscriber_count,
    "Comments": all_coments
    
}
# Save the record to the collection
collection.insert_one(youtube_data)

print(f"Video details and comments scraped from '{video_title}' saved in the database youtube-data.")
