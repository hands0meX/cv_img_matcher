FROM python:3.8.18-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6
ENV FLASK_APP=server/app.py
EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]
# CMD ["bash", "-c", "while true; do sleep 3600; done"]