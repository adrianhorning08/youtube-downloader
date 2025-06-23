from flask import Flask, request, jsonify
from yt_dlp import YoutubeDL
from supabase import create_client
import os
import time
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Load Supabase credentials from env vars
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Create Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return 'YouTube Downloader API is running!'

@app.route('/download', methods=['GET'])
def download():
    url = request.args.get('url')

    if not url:
        return jsonify({'error': 'Missing URL'}), 400

    timestamp = int(time.time())
    file_name = f"video-{timestamp}.mp4"
    file_path = file_name

    ydl_opts = {
        'format': 'bv*+ba/best',
        'merge_output_format': 'mp4',
        'outtmpl': file_path,
    }

    try:
        # Download video
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Upload to Supabase
        bucket = "youtube-videos"
        supabase.storage.from_(bucket).upload(
            file_name,
            file_path,
            {"content-type": "video/mp4"}
        )

        # Remove local file
        os.remove(file_path)

        # Return public URL
        public_url = f"{SUPABASE_URL}/storage/v1/object/public/{bucket}/{file_name}"
        return jsonify({'message': '✅ Uploaded!', 'url': public_url})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

