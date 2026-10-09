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
        # YouTube TV ve GData istemcilerini taklit ederek engeli aşmayı dener
        'extractor_args': {
            'youtube': {
                'player_client': ['tv', 'mweb', 'android'],
                'skip': ['webpage']
            }
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
