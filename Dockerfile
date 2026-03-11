FROM python:3.10-slim

# تثبيت الأدوات اللازمة للنظام
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# إعداد مستخدم بصلاحيات محدودة للأمان
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app

# تثبيت مكتبات بايثون
COPY --chown=user:user requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --upgrade -r requirements.txt

# نسخ الكود
COPY --chown=user:user . .

# تشغيل الـ API (Render يستخدم المنفذ 10000 غالباً أو يحدده تلقائياً)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "10000"]
