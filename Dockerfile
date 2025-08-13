# Gunakan image ringan
FROM python:3.12-slim

# Install dependency sistem (untuk Pillow & TensorFlow)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set direktori kerja
WORKDIR /app

# Salin requirements terlebih dahulu agar caching efisien
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Salin hanya file penting (lebih cepat dan hemat space)
COPY app.py ./app.py
COPY model ./model

# Flask akan jalan di port 8080
EXPOSE 8080

# Jalankan aplikasi
CMD ["python", "app.py"]