"""
RetailPulse AI — One-Command Launcher
--------------------------------------
Builds the React frontend (if needed) then starts the FastAPI server.
Everything runs on a single port: http://localhost:8000

Usage:
    python start.py              # auto-build if dist/ is missing, then serve
    python start.py --rebuild    # force rebuild of React app before serving
    python start.py --skip-build # skip React build (use existing dist/)
    python start.py --port 9000  # run on a custom port
"""

import os
import sys
import shutil
import subprocess
import argparse
import uvicorn

ROOT = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(ROOT, "frontend")
FRONTEND_DIST = os.path.join(FRONTEND_DIR, "dist")


def find_npm() -> str:
    """Find npm executable, checking the portable Node.js location first."""
    candidates = [
        os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs", "nodejs", "npm.cmd"),
        "npm.cmd",   # on PATH (Windows)
        "npm",       # on PATH (Linux/macOS)
    ]
    for npm in candidates:
        if shutil.which(npm):
            return npm
        if os.path.exists(npm):
            return npm
    return None


def build_frontend(force: bool = False) -> bool:
    """Build the React app with Vite. Returns True on success."""
    if not force and os.path.exists(FRONTEND_DIST):
        print("✅  React build already exists at frontend/dist — skipping build.")
        print("    (Use --rebuild to force a fresh build)\n")
        return True

    npm = find_npm()
    if not npm:
        print("⚠️  npm not found. Cannot build frontend.")
        print("   Install Node.js or add it to PATH, then run: cd frontend && npm run build")
        return False

    print("📦  Installing frontend dependencies...")
    env = os.environ.copy()
    env["NODE_TLS_REJECT_UNAUTHORIZED"] = "0"  # handles corporate proxy / self-signed certs

    result = subprocess.run(
        [npm, "install", "--no-audit", "--no-fund"],
        cwd=FRONTEND_DIR,
        env=env,
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print(f"❌  npm install failed:\n{result.stderr}")
        return False

    print("🔨  Building React app (Vite production build)...")
    result = subprocess.run(
        [npm, "run", "build"],
        cwd=FRONTEND_DIR,
        env=env,
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print(f"❌  Frontend build failed:\n{result.stderr}\n{result.stdout}")
        return False

    print("✅  Frontend build succeeded.\n")
    return True


def main():
    parser = argparse.ArgumentParser(description="RetailPulse AI — Unified launcher")
    parser.add_argument("--rebuild",     action="store_true", help="Force rebuild the React app before starting")
    parser.add_argument("--skip-build",  action="store_true", help="Skip React build entirely")
    parser.add_argument("--port",        type=int, default=8000, help="Port to run on (default: 8000)")
    parser.add_argument("--host",        type=str, default="0.0.0.0", help="Host to bind (default: 0.0.0.0)")
    parser.add_argument("--reload",      action="store_true", help="Enable uvicorn auto-reload (development mode)")
    args = parser.parse_args()

    print("=" * 60)
    print("  RetailPulse AI — Autonomous Retail Intelligence Platform")
    print("=" * 60)
    print()

    if not args.skip_build:
        ok = build_frontend(force=args.rebuild)
        if not ok:
            print("\n⚠️  Continuing without frontend build. API will still be available.")
    else:
        print("⏭️  Skipping frontend build (--skip-build flag set).\n")

    dist_exists = os.path.exists(FRONTEND_DIST)
    print("🚀  Starting RetailPulse AI server...\n")
    if dist_exists:
        print(f"   🌐  Dashboard  →  http://localhost:{args.port}/")
    print(f"   📋  API Docs   →  http://localhost:{args.port}/docs")
    print(f"   📄  ReDoc      →  http://localhost:{args.port}/redoc")
    print(f"   🔌  API Base   →  http://localhost:{args.port}/api/")
    print()

    uvicorn.run(
        "backend.app.main:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level="info"
    )


if __name__ == "__main__":
    main()
