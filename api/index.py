from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
import yt_dlp

app = FastAPI()

@app.get("/api/download")
def download(url: str):
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            # بدل ما نحمل على السيرفر، هندي للمستخدم رابط التحميل المباشر
            download_url = info.get('url')
            return RedirectResponse(url=download_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
