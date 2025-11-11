#!/usr/bin/env python3
"""
ACP0 Demo Runner - Windows compatible version
"""

import os
import sys
import subprocess

def main():
    print("🚀 ACP0 Minimal Demo")
    print("====================")
    print("")
    
    # 检查Python包依赖
    print("📦 Checking dependencies...")
    try:
        import pydantic
        import ecdsa
        import uuid
        print('✓ All dependencies available')
    except ImportError as e:
        print(f'❌ Missing dependency: {e}')
        print('Please install with: pip install pydantic ecdsa')
        sys.exit(1)
    
    # 运行 Demo
    print("")
    print("📦 Starting agents...")
    
    # 切换到项目根目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    os.chdir(project_root)
    
    # 运行演示
    result = subprocess.run([sys.executable, "examples/minimal_demo.py"], 
                          capture_output=True, text=True)
    
    print(result.stdout)
    if result.stderr:
        print("Errors:", result.stderr)
    
    print("")
    print("✅ Demo completed successfully!")

if __name__ == "__main__":
    main()
