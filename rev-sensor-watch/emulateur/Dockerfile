FROM python:alpine
WORKDIR /app
COPY src/watch.html src/watch.js src/watch.wasm src/favicon.ico ./
EXPOSE 8000
CMD ["python3", "-m", "http.server"]
