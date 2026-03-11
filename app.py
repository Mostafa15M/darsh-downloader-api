import os
import uuid
import yt_dlp
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="YoutDarsh Downloader")

# تفعيل CORS لتتمكن من استخدام الـ API في موقعك (Blogger)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# مجلد مؤقت للتحميل
DOWNLOAD_DIR = "/tmp/downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def cleanup_file(path: str):
    """حذف الملف بعد إرساله للمستخدم"""
    if os.path.exists(path):
        os.remove(path)

@app.get("/")
def home():
    return {"status": "online", "message": "YoutDarsh API is ready"}

@app.get("/download")
async def download_video(url: str, background_tasks: BackgroundTasks):
    file_id = str(uuid.uuid4())
    output_template = f"{DOWNLOAD_DIR}/{file_id}.%(ext)s"

    # إعدادات تخطي الحظر والقيود
    ydl_opts = {
        'format': 'best',
        'outtmpl': output_template,
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
            original_name = f"{info.get('title', 'video')}.{info.get('ext', 'mp4')}"

        # إضافة مهمة الحذف في الخلفية
        background_tasks.add_task(cleanup_file, file_path)

        return FileResponse(
            path=file_path,
            filename=original_name,
            media_type='application/octet-stream'
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
