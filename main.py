from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp

app = FastAPI(title="COLoad API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "ok", "message": "Video Downloader API Calisiyor"}

@app.get("/api/download")
def get_video_info(url: str = Query(..., description="Indirilecek video baglantisi")):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'skip_download': True,
        'format': 'best',
        # YouTube bot engellerini taklit ederek aşmak için eklenen ayarlar:
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web']
            }
        },
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            return {
                "success": True,
                "title": info.get('title'),
                "thumbnail": info.get('thumbnail'),
                "duration": info.get('duration'),
                "uploader": info.get('uploader'),
                "download_link": info.get('url')
            }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Video bilgisi alınamadı: {str(e)}")
