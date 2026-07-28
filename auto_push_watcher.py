import subprocess
import time
import datetime
import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
CHECK_INTERVAL = 10  # Cek setiap 10 detik

def run_git_command(args):
    try:
        result = subprocess.run(
            ["git"] + args,
            cwd=PROJECT_DIR,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Git command error: {e.stderr.strip() if e.stderr else e}")
        return None

def check_and_push():
    status = run_git_command(["status", "--porcelain"])
    if status:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{now}] Perubahan terdeteksi. Mengunggah otomatis ke GitHub...")
        
        run_git_command(["add", "."])
        commit_msg = f"auto-update: {now}"
        run_git_command(["commit", "-m", commit_msg])
        
        push_res = run_git_command(["push", "origin", "main"])
        if push_res is not None:
            print(f"[{now}] ✅ Berhasil di-push ke GitHub!")
        else:
            print(f"[{now}] ⚠️ Push gagal (Pastikan remote origin GitHub sudah terpasang).")

if __name__ == "__main__":
    print(f"==================================================")
    print(f"🚀 Auto Push GitHub Daemon Aktif (Cek tiap {CHECK_INTERVAL}s)")
    print(f"Folder Project: {PROJECT_DIR}")
    print(f"==================================================")
    while True:
        try:
            check_and_push()
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(CHECK_INTERVAL)
