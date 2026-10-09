from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
import yt_dlp

app = FastAPI(title="COLoad API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Eğer CSS, JS veya resim klasörünüz varsa (örn: static klasörü) sorunsuz yüklenmesi için:
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home():
    # Ana sayfaya girildiğinde direkt index.html dosyasını döndürür
    return FileResponse("index.html")

@app.get("/api/download")
def get_video_info(url: str = Query(..., description="Indirilecek video baglantisi")):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'skip_download': True,
        'format': 'best',
        'nocheckcertificate': True,
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'ios', 'mweb'],
                'skip': ['configs', 'webpage']
            }
        },
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        }
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
