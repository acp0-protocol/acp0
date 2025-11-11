#!/bin/bash
set -e

cd "$(dirname "$0")/.."

echo "🚀 ACP0 Minimal Demo"
echo "===================="
echo ""

# 检查依赖
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found"
    exit 1
fi

# 检查Python包依赖
echo "📦 Checking dependencies..."
python3 -c "
try:
    import pydantic
    import ecdsa
    import uuid
    print('✓ All dependencies available')
except ImportError as e:
    print(f'❌ Missing dependency: {e}')
    print('Please install with: pip install pydantic ecdsa')
    exit(1)
"

# 运行 Demo
echo ""
echo "📦 Starting agents..."
python3 examples/minimal_demo.py

echo ""
echo "✅ Demo completed successfully!"
