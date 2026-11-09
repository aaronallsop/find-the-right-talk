# The lean hosted page. Build from the repository's top folder:
#     docker build -f hosted/Dockerfile -t find-the-right-talk .
# No key, token or settings file goes into the image (see hosted/Dockerfile.dockerignore); the Elastic address and
# key arrive at run time as the environment variables ES_CLOUD_URL and ES_CLOUD_API_KEY, from a Kubernetes secret.
# No torch and no meaning model: words, ELSER and Jina only.
FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1
WORKDIR /app
COPY hosted/requirements.txt hosted/requirements.txt
RUN pip install -r hosted/requirements.txt
COPY ftrt ftrt
COPY data data
COPY hosted hosted
RUN useradd --uid 10001 --no-create-home app
USER 10001
ENV FTRT_ENGINE=cloud PORT=8080
EXPOSE 8080
CMD ["sh", "-c", "exec gunicorn --bind 0.0.0.0:${PORT} --workers 1 --threads 16 --timeout 120 hosted.app:app"]
