import os
import time
import uuid
import subprocess
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from supabase import create_client
from multiprocessing import Process, Queue
import random

load_dotenv()

app = Flask(__name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
BUCKET = "youtube-videos"
PROXY = os.getenv("RESIDENTIAL_PROXY") or ""




def download_worker(url, proxy, filename, queue):
    try:
        args = [
            "yt-dlp",
            "-o", filename,
            "--merge-output-format", "mp4",
            "--proxy", proxy,
            "--format", "bestvideo[ext=mp4][vcodec^=avc1]+bestaudio[ext=m4a]/best[ext=mp4][vcodec^=avc1]",
            "-N", "4",
            url
        ]
        result = subprocess.run(args, capture_output=True)
        if result.returncode != 0:
            raise Exception(result.stderr.decode())

        supabase.storage.from_(BUCKET).upload(
            filename,
            filename,
            {"content-type": "video/mp4"}
        )

        os.remove(filename)

        video_url = f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET}/{filename}"
        queue.put({"success": True, "url": video_url})
    except Exception as e:
        queue.put({"success": False, "error": str(e)})


@app.route("/download", methods=["GET"])
def download():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Missing URL"}), 400

    unique_id = uuid.uuid4().hex
    filename = f"video-{unique_id}.mp4"
    queue = Queue()

    p = Process(target=download_worker, args=(url, PROXY, filename, queue))
    p.start()
    p.join(timeout=180)

    if p.is_alive():
        p.terminate()
        return jsonify({"error": "Download timed out"}), 500

    result = queue.get()
    if result.get("success"):
        return jsonify({"message": "✅ Uploaded!", "url": result["url"]})
    else:
        return jsonify({"error": result.get("error")}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5005, debug=True)
