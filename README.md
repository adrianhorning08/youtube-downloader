This is my open sourced code to download the mp4 of a YouTube video.

I deploy this on render.com

Use this to run:

```
python3 -m venv venv
source venv/bin/activate

python3 app.py

pip install -r requirements.txt
```

Environment Variables you need:

```
SUPABASE_URL
SUPABASE_KEY
RESIDENTIAL_PROXY
```

I'm using Evomi core residential proxy: https://evomi.com/product/residential-proxies

I'm using Supabase to store everything, use whatever storage you like.

Brought to you by https://scrapecreators.com/
