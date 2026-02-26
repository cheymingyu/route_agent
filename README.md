## Route Agent Deployment

### 1) Environment variables
```bash
cp .env.example .env
```

Fill `.env` with actual API keys:
- `ODSAY_API_KEY`
- `NAVER_MAPS_CLIENT_ID`
- `NAVER_MAPS_CLIENT_SECRET`
- `NAVER_CLIENT_ID`
- `NAVER_CLIENT_SECRET`

### 2) Start with Docker Compose
```bash
docker compose up -d --build
```

The API is exposed at `http://localhost:8000`.

### 3) Pull Ollama model (first run)
```bash
docker exec -it route-agent-ollama ollama pull qwen3:4b-instruct
```

If you want another model, update `OLLAMA_MODEL` in `.env` and pull that model.

### 4) Health check
```bash
curl -X POST http://localhost:8000/agent-test \
  -H "Content-Type: application/json" \
  -d '{"text":"서울역에서 강남역 가는 길에 한식집 추천해줘"}'
```

### 5) Logs / stop
```bash
docker compose logs -f app
docker compose down
```
