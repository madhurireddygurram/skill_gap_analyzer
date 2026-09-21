"""
Run this file to start both servers at once:
    python run.py
"""
import subprocess, sys, os, time, webbrowser, shutil

# Prevent UnicodeEncodeError on Windows command prompt / PowerShell with cp1252
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT    = os.path.dirname(os.path.abspath(__file__))
BACKEND = os.path.join(ROOT, "backend")

def get_python_interpreter():
    """Find the Python interpreter that has project dependencies installed."""
    try:
        import uvicorn, streamlit  # noqa: F401
        return sys.executable
    except ImportError:
        pass

    py_bin = shutil.which("py")
    if py_bin:
        res = subprocess.run(
            [py_bin, "-3.12", "-c", "import sys; print(sys.executable)"],
            capture_output=True,
            text=True,
        )
        if res.returncode == 0 and res.stdout.strip():
            candidate = res.stdout.strip()
            chk = subprocess.run([candidate, "-c", "import uvicorn, streamlit"], capture_output=True)
            if chk.returncode == 0:
                return candidate

    return sys.executable

def main():
    python_exe = get_python_interpreter()

    print(f"Using Python: {python_exe}")
    print("Starting FastAPI backend on http://localhost:8000 ...")
    api = subprocess.Popen(
        [python_exe, "-m", "uvicorn", "main:app", "--reload", "--port", "8000"],
        cwd=BACKEND
    )

    time.sleep(2)

    print("Starting Streamlit frontend on http://localhost:8501 ...")
    ui = subprocess.Popen(
        [python_exe, "-m", "streamlit", "run", "app.py"],
        cwd=ROOT
    )

    time.sleep(3)
    webbrowser.open("http://localhost:8501")

    print("\n[OK] Both servers running.")
    print("   Streamlit  -> http://localhost:8501")
    print("   API docs   -> http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop both.\n")

    try:
        api.wait()
    except KeyboardInterrupt:
        print("\nShutting down...")
        api.terminate()
        ui.terminate()

if __name__ == "__main__":
    main()
