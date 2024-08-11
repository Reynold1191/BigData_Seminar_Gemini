from dotenv import load_dotenv

import os
import pandas as pd
import facebook_scraper as fs
import googleapiclient.discovery as gd

load_dotenv()

GOOGLE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# Disable OAuthlib's HTTPS verification when running locally.
# *DO NOT* leave this option enabled in production.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

def get_fb_post_id(url):
    start = url.find("pfbid")
    end = url.find("?", start)

    # Extract the part of the URL
    if start != -1 and end != -1:
        extracted_id = url[start:end]
    else:
      extracted_id = url[start:] if start != -1 else None

    return extracted_id

def scrape_fb_post_comments(post_id, max_comments):
    max_comments = 20

    gen = fs.get_posts(
        post_urls=[post_id],
        options={"comments": max_comments, "allow_extra_requests": False}
    )

    # take 1st element of the generator which is the post we requested
    post = next(gen)

    # extract the comments part
    comments = post['comments_full']

        
    df = pd.DataFrame(comments)
    # df.drop(columns=['replies'], inplace=True)

    return df

def get_youtube_video_id(url):
    start = url.find("v=")
    end = url.find("&", start)

    # Extract the part of the URL
    if start != -1 and end != -1:
        extracted_id = url[start+2:end]
    else:
        extracted_id = url[start+2:] if start != -1 else None

    return extracted_id

def get_ytb_livestream_comments(video_id, max_comments):
    api_service_name = "youtube"
    api_version = "v3"

    youtube = gd.build(api_service_name, api_version, developerKey=GOOGLE_API_KEY)

    request = youtube.videos().list(
        part="liveStreamingDetails",
        id=video_id,
    )
    response = request.execute()
    print(response)

    activeLiveChatId = response['items'][0]['liveStreamingDetails']['activeLiveChatId']

    request = youtube.liveChatMessages().list(
        liveChatId=activeLiveChatId,
        part="snippet",
        maxResults=max_comments
    )

    response = request.execute()

    comments = [item['snippet']['displayMessage'] for item in response['items'] if 'displayMessage' in item['snippet']]

    df = pd.DataFrame(comments, columns=['comment_text'])

    return df

def get_ytb_video_comments(video_id, max_comments):
    api_service_name = "youtube"
    api_version = "v3"

    youtube = gd.build(api_service_name, api_version, developerKey=GOOGLE_API_KEY)

    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=max_comments
    )

    response = request.execute()

    comments = [item['snippet']['topLevelComment']['snippet']['textOriginal'] for item in response['items']]

    print(comments)

    df = pd.DataFrame(comments, columns=['comment_text'])

    return df
