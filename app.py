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


evomiStaticResidentialProxies = [
  "adrian:4ov6l2temn2@161.115.234.208:12345",
  "adrian:ayb2k9vhlca@161.115.234.209:12345",
  "adrian:hiepfa20m7r@161.115.234.210:12345",
  "adrian:4trvj2vygd@161.115.234.211:12345",
  "adrian:2y20nfmv05d@161.115.234.212:12345",
  "adrian:vyhkfoo78gc@161.115.234.213:12345",
  "adrian:f1pnmcf59kk@161.115.234.214:12345",
  "adrian:hynuf8svbp4@161.115.234.215:12345",
  "adrian:cn5ti5keblk@161.115.234.216:12345",
  "adrian:696c06wtcbw@161.115.234.217:12345",
  "adrian:nvvggcvkyd@161.115.234.218:12345",
  "adrian:r51wbx2ym3@161.115.234.219:12345",
  "adrian:uiebtukt4q@161.115.234.220:12345",
  "adrian:jl2g9qdst2h@161.115.234.221:12345",
  "adrian:3whwjh7vpkk@161.115.234.222:12345",
  "adrian:p0t12zn8plr@161.115.234.223:12345",
  "adrian:g0qn0k2q52s@161.115.234.224:12345",
  "adrian:zmesvxchqtr@161.115.234.225:12345",
  "adrian:fzt1f884m87@161.115.234.226:12345",
  "adrian:p5kex25dawh@161.115.234.227:12345",
  "adrian:pz6ucn9ogz@161.115.239.100:12345",
  "adrian:f05mykp558@161.115.239.102:12345",
  "adrian:4s9bpqi1d2p@161.115.239.101:12345",
  "adrian:phy0isxof1r@161.115.239.103:12345",
  "adrian:65j8s3z8ydr@161.115.239.104:12345",
  "adrian:gop28nobiut@161.115.239.105:12345",
  "adrian:58c8bof35im@161.115.239.107:12345",
  "adrian:d40pg7knz7@161.115.239.108:12345",
  "adrian:bxnqyxibslw@161.115.239.106:12345",
  "adrian:jg5p99k6l8l@161.115.239.110:12345",
  "adrian:ak8111g3a@161.115.239.109:12345",
  "adrian:b88oeoruwak@161.115.239.251:12345",
  "adrian:f6nv740xi1@161.115.239.252:12345",
  "adrian:pjnhczas6jr@161.115.239.250:12345",
  "adrian:x1e6bwubcu@161.115.239.253:12345",
  "adrian:r7tt36qhj3@161.115.239.254:12345",
  "adrian:vnnrvzcoh3d@161.115.239.224:12345",
  "adrian:um780aqh43@161.115.239.227:12345",
  "adrian:wht2l9adaf@161.115.239.225:12345",
  "adrian:km390t78i@161.115.239.228:12345",
  "adrian:x4o94sgdkzg@161.115.239.229:12345",
  "adrian:wmqsohrb7kp@161.115.239.230:12345",
  "adrian:mzvqs6qb90l@161.115.239.232:12345",
  "adrian:i0gxrze8zjg@161.115.239.231:12345",
  "adrian:mu7j05hu66@161.115.239.233:12345",
  "adrian:o6sf0q6kkk@161.115.239.234:12345",
  "adrian:goru97gi4od@161.115.239.235:12345",
  "adrian:uot4ze8qug9@161.115.239.236:12345",
  "adrian:axfgdzr64w8@161.115.239.237:12345",
  "adrian:mx2ofvu1ijl@161.115.239.226:12345",
  "adrian:w1r3h8c3cq@161.115.239.238:12345",
  "adrian:aghwghba5c9@161.115.239.239:12345",
  "adrian:etwfj9gjdjg@161.115.239.240:12345",
  "adrian:2rpm155gsx5@161.115.239.241:12345",
  "adrian:bgw9c9t5dxi@161.115.239.244:12345",
  "adrian:ppbr9rf91hq@161.115.239.243:12345",
  "adrian:g0abmpgdvj5@161.115.239.246:12345",
  "adrian:2w6su0ks88f@161.115.239.245:12345",
  "adrian:f0oibif1xj@161.115.239.242:12345",
  "adrian:0hc5t6hmufzn@161.115.239.248:12345",
  "adrian:qmw1oslvzl@161.115.239.247:12345",
  "adrian:8nocfao8mjk@161.115.239.249:12345",
  "adrian:2bmn9do8tt8@161.115.239.95:12345",
  "adrian:i8thtwb8qka@161.115.239.117:12345",
  "adrian:cmxfe2ht9h9@161.115.239.77:12345",
  "adrian:4lg95j6bmza@161.115.239.79:12345",
  "adrian:wqsyjm7mc1d@161.115.239.80:12345",
  "adrian:wr4tm59tnrj@161.115.239.81:12345",
  "adrian:9ing6zytmqw@161.115.239.78:12345",
  "adrian:0qx3gkbquhuq@161.115.239.82:12345",
  "adrian:nmy1bzjwis7@161.115.239.85:12345",
  "adrian:m6d9kaevldi@161.115.239.84:12345",
  "adrian:iy9l0kcze7m@161.115.239.87:12345",
  "adrian:m8mv2mz82fr@161.115.239.86:12345",
  "adrian:gjo1ezen735@161.115.239.83:12345",
  "adrian:raxk5qx2s4j@161.115.239.89:12345",
  "adrian:v930eo27ki@161.115.239.90:12345",
  "adrian:8oylu6ob3ct@161.115.239.91:12345",
  "adrian:45e6oko7nep@161.115.239.93:12345",
  "adrian:qlmg65rfit@161.115.239.88:12345",
  "adrian:2rmgh7leldp@161.115.239.94:12345",
  "adrian:8z62uzvqf5@161.115.239.92:12345",
  "adrian:ebkqjll5xtd@161.115.239.118:12345",
  "adrian:pzeas8f5lf@161.115.239.116:12345",
  "adrian:vznf5wzif3@161.115.239.119:12345",
  "adrian:lkfppjzaci@161.115.239.121:12345",
  "adrian:vu55sce5at@161.115.239.123:12345",
  "adrian:duuqf69s1h@161.115.239.124:12345",
  "adrian:6g2z1q8ojur@161.115.239.126:12345",
  "adrian:kz7rgi3w2tr@161.115.239.125:12345",
  "adrian:8uzxeq5szm@161.115.239.122:12345",
  "adrian:u6z9f2jq31j@161.115.239.127:12345",
  "adrian:0jflsnpt25f@161.115.239.129:12345",
  "adrian:xgt0h4rb88r@161.115.239.131:12345",
  "adrian:yvegy4sttsk@161.115.239.132:12345",
  "adrian:u5itmsq8mif@161.115.239.134:12345",
  "adrian:ke0w524k719@161.115.239.136:12345",
  "adrian:0iejp26rcf2g@161.115.239.137:12345",
  "adrian:dtyq3kid4sq@161.115.239.140:12345",
  "adrian:jywfj7j68u@161.115.239.141:12345",
  "adrian:z38h6g8420q@161.115.239.142:12345",
  "adrian:vrwszeu48vo@161.115.239.143:12345",
  "adrian:jl91nv0r04m@161.115.239.144:12345",
  "adrian:6ag5n7v7c5t@161.115.239.146:12345",
  "adrian:dk6d9udqtb@161.115.239.147:12345",
  "adrian:rlhdqkkyy5p@161.115.239.145:12345",
  "adrian:uiy5psitwda@161.115.239.149:12345",
  "adrian:5aytbmuju9p@161.115.239.150:12345",
  "adrian:m5w3j44ui7m@161.115.239.152:12345",
  "adrian:kayx6knp1ld@161.115.239.148:12345",
  "adrian:uquvkdq19po@161.115.239.151:12345",
  "adrian:cxqruc4r95@161.115.239.153:12345",
  "adrian:i0mgf7704fj@161.115.239.155:12345",
  "adrian:eh0y7iwx6u4@161.115.239.154:12345",
  "adrian:73wfj4ozlug@161.115.239.158:12345",
  "adrian:zzvujyaq1w8@161.115.239.157:12345",
  "adrian:r6ucjnjoqdk@161.115.239.160:12345",
  "adrian:frhaxj6lb0f@161.115.239.159:12345",
  "adrian:ruv2byf3jlc@161.115.239.156:12345",
  "adrian:fw6ebcnj1ju@161.115.239.162:12345",
];

def getEvomiStaticResidentialProxyUrl():
  randomIndex = random.randint(0, len(evomiStaticResidentialProxies) - 1)
  return f"http://{evomiStaticResidentialProxies[randomIndex]}"




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
