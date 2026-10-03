from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp

app = FastAPI(title="Video Downloader API")

# Sitenizden (Frontend) gelen isteklere izin vermek için CORS ayarı
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
def get_video_info(url: str = Query(..., description="Indirilecek video bağlantısı")):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'skip_download': True,
        'format': 'best',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Formatlardan doğrudan video/ses linklerini ayıkla
            formats = []
            for f in info.get('formats', []):
                # Sadece doğrudan indirme linki (url) içeren formatları al
                if f.get('url') and f.get('ext') in ['mp4', 'm4a', 'webm', 'mp3']:
                    formats.append({
                        'format_id': f.get('format_id'),
                        'ext': f.get('ext'),
                        'resolution': f.get('resolution') or f.get('format_note'),
                        'filesize': f.get('filesize'),
                        'download_url': f.get('url')
                    })

            return {
                "success": True,
                "title": info.get('title'),
                "thumbnail": info.get('thumbnail'),
                "duration": info.get('duration'),
                "uploader": info.get('uploader'),
                "download_link": info.get('url'),  # En yüksek kaliteli doğrudan link
                "all_formats": formats[:10]       # Seçenekler için ilk 10 format
            }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Video bilgisi alınamadı: {str(e)}")
