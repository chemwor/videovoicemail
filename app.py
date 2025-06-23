from flask import Flask, request, send_file, jsonify
from PIL import Image, ImageDraw, ImageFont
import uuid
import os
import requests
import time
import cv2

app = Flask(__name__)





def download_video(video_url, path="temp_video.mp4"):
    response = requests.get(video_url)
    with open(path, "wb") as f:
        f.write(response.content)
    return path

def extract_thumbnail(video_path, output_image="thumbnail.jpg"):
    cap = cv2.VideoCapture(video_path)
    success, frame = cap.read()
    if success:
        cv2.imwrite(output_image, frame)
    cap.release()
    return output_image


def download_thumbnail(thumbnail_url, filename="thumbnail.jpg"):
    response = requests.get(thumbnail_url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"📥 Thumbnail saved as {filename}")
    else:
        print(f"❌ Failed to download thumbnail. Status code: {response.status_code}")


def create_tavus_video(script, video_name="Demo Video", background_url=None):
    url = "https://tavusapi.com/v2/videos"

    payload = {
        "replica_id": "rca8a38779a8",
        "script": script,
        "video_name": video_name,
    }

    if background_url:
        payload["background_url"] = background_url

    headers = {
        "x-api-key": "39feb278add5444989379beefc9fa128",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    print("🔁 Video generation response:", data)
    return data.get("video_id")


def check_tavus_video_status(video_id):
    url = f"https://tavusapi.com/v2/videos/{video_id}"
    headers = {
        "x-api-key": "39feb278add5444989379beefc9fa128"
    }

    while True:
        response = requests.get(url, headers=headers)
        data = response.json()
        print("📡 Status:", data.get("status"))

        if data.get("status") == "ready":
            print("✅ Video ready:", data.get("hosted_url"))
            return data.get("hosted_url")
        elif data.get("status") == "error":
            raise Exception("❌ Tavus video generation failed.")

        time.sleep(5)

# Example usage
script = "Hey Chris we were able to get Landon 500k in funding with just bank statements. Take a look at this"

video_id = create_tavus_video(script)
video_url = check_tavus_video_status(video_id)
video_path = download_video(video_url)
thumbnail_path = extract_thumbnail(video_path)
print(f"🖼️ Thumbnail saved at: {thumbnail_path}")


if __name__ == '__main__':
    app.run(debug=True, port=5000)





