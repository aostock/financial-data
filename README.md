# run

```
source .venv/bin/activate
fastapi dev main.py

```

# mcp client config

```json
{
  "mcpServers": {
    "finance-data": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "http://127.0.0.1:8000/mcp", "--header", "Authorization:Bearer secret-token"]
    }
  }
}
# 生产环境运行

```

uvicorn main:app --host 0.0.0.0 --port 8000

```

```
