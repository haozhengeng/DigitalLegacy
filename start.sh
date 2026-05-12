#!/bin/bash
# DigitalLegacy - 数字遗产管家 一键启动脚本

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
export PATH="$HOME/.local/node/bin:$PATH"

echo "==================================="
echo "  数字遗产管家 DigitalLegacy v2"
echo "==================================="

# 启动后端
echo "[1/2] 启动后端 API (port 8000)..."
cd "$PROJECT_DIR/backend"
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# 等待后端启动
sleep 2

# 启动前端
echo "[2/2] 启动前端 (port 5173)..."
cd "$PROJECT_DIR/frontend"
npx vite --host &
FRONTEND_PID=$!

echo ""
echo "==================================="
echo "  后端: http://localhost:8000"
echo "  前端: http://localhost:5173"
echo "  API文档: http://localhost:8000/docs"
echo "==================================="
echo "  按 Ctrl+C 停止所有服务"
echo "==================================="

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" SIGINT SIGTERM
wait
