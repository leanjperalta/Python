#!/usr/bin/env python3

import csv
import requests
import os

def get_uploads_playlist_id(channel_id, api_key):
    url = f"https://www.googleapis.com/youtube/v3/channels?part=contentDetails&id={channel_id}&key={api_key}"
    response = requests.get(url)
    data = response.json()
    if "items" not in data or not data["items"]:
        raise ValueError("Check CHANNEL_ID & API_KEY.")
    return data["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

def get_all_video_ids(playlist_id, api_key):
    video_ids = []
    next_page_token = None
    while True:
        url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={playlist_id}&key={api_key}&maxResults=50"
        if next_page_token:
            url += f"&pageToken={next_page_token}"
        response = requests.get(url)
        data = response.json()
        video_ids.extend([item["snippet"]["resourceId"]["videoId"] for item in data["items"]])
        next_page_token = data.get("nextPageToken")
        if not next_page_token:
            break
    return video_ids

def get_video_stats(video_ids, api_key):
    stats = []
    for i in range(0, len(video_ids), 50):
        batch = video_ids[i:i+50]
        url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&id={','.join(batch)}&key={api_key}"
        response = requests.get(url)
        data = response.json()
        for item in data["items"]:
            stats.append({
                "title": item["snippet"]["title"],
                "views": item["statistics"]["viewCount"]
            })
    return stats

def main():
    API_KEY = "xxxxxx"
    CHANNEL_ID = "UChKJaUFTKfw5O8JtQmF4Q6g"  


    output_dir = "/" #set dir 
    output_filename = "youtube_video_stats.csv"
    output_path = os.path.join(output_dir, output_filename)

    try:
        playlist_id = get_uploads_playlist_id(CHANNEL_ID, API_KEY)
        video_ids = get_all_video_ids(playlist_id, API_KEY)
        stats = get_video_stats(video_ids, API_KEY)

        
#        os.makedirs(output_dir, exist_ok=True)

        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Title', 'Views']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for stat in stats:
                writer.writerow({'Title': stat['title'], 'Views': stat['views']})

        print(f"CSV file '{output_path}' created!")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
