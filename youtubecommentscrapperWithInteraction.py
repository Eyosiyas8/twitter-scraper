import os
import pickle
import requests
from googleapiclient.discovery import build
from pymongo import MongoClient

# Initializing mongo db client
client = MongoClient('mongodb://localhost:27017/')
db = client['youtube-data']
collection = db['youtube']

# Set up the YouTube Data API v3 credentials
API_KEY = "AIzaSyCbGeJsInTEzEaW0Yib2MFi9Jn-lB4A46c"  # Replace with your own API key
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# Set up the output file path
OUTPUT_FILE = "comments.txt"

# Set up the YouTube Data API client
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)

# Input the YouTube video URL from the user
VIDEO_URL = input("Enter the YouTube video URL: ")

# Extract the video ID from the YouTube video URL
video_id = VIDEO_URL.split("v=")[1]

# Request the video details using the YouTube Data API
video_response = youtube.videos().list(part="snippet, statistics", id=video_id).execute()
video_title = video_response["items"][0]["snippet"]["title"]
video_description = video_response["items"][0]["snippet"]["description"]
video_published_date = video_response["items"][0]["snippet"]["publishedAt"]
video_url = f"https://www.youtube.com/watch?v={video_id}"
video_likes = video_response["items"][0]["statistics"]["likeCount"]
video_views = video_response["items"][0]["statistics"]["viewCount"]
video_shares = int(video_views) // 50  # Assume 1 share for every 50 views

# Request the channel details using the YouTube Data API
channel_id = video_response["items"][0]["snippet"]["channelId"]
channel_response = youtube.channels().list(part="statistics", id=channel_id).execute()
subscriber_count = channel_response["items"][0]["statistics"]["subscriberCount"]

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
        comment = comment_thread["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        comments.append(comment)

    if "nextPageToken" in comment_threads:
        next_page_token = comment_threads["nextPageToken"]
    else:
        break

    # Appending all the comments to one list
    all_coments = []
    for comment in comments:
        all_coments.append(comment)

# Save the comments to a file
# with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
#     file.write(f"Video Title: {video_title}\n")
#     file.write(f"Video URL: {video_url}\n")
#     file.write(f"Description: {video_description}\n")
#     file.write(f"Date of Post: {video_published_date}\n")
#     file.write(f"Likes: {video_likes}\n")
#     file.write(f"Shares: {video_shares}\n")
#     file.write(f"Subscriber Count: {subscriber_count}\n\n")
#     file.write("Comments:\n")
#     for comment in comments:
#         file.write(f"- {comment}\n")

# Create a dictionary to store all the data
youtube_data = {
    "Video Title": video_title,
    "Video URL": video_url,
    "Description": video_description,
    "Date of Post": video_published_date,
    "Likes": video_likes,
    "Shares": video_shares,
    "Subscriber Count": subscriber_count,
    "Comments": all_coments
    
}
# Save the record to the collection
collection.insert_one(youtube_data)

# print(f"Comments scraped from '{video_title}' saved to '{os.path.abspath(OUTPUT_FILE)}'.")
