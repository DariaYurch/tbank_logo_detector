FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir \
    --index-url https://download.pytorch.org/whl/cpu \
    torch==2.9.0 torchvision==0.24.0

RUN sed -e '/^torch==/d' -e '/^torchvision==/d' requirements.txt > requirements_no_torch.txt \
    && pip install --no-cache-dir -r requirements_no_torch.txt
    
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg libsm6 libxext6 && \
    rm -rf /var/lib/apt/lists/*

COPY app ./app
COPY data ./data

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
