@echo off
echo ==============================================
echo   Pushing project updates to GitHub...
echo ==============================================

git add .
set /p commit_msg="Masukkan pesan commit (tekan Enter untuk default 'update project'): "
if "%commit_msg%"=="" set commit_msg=update project

git commit -m "%commit_msg%"
git push origin main

echo ==============================================
echo   Selesai! Perubahan telah di-push ke GitHub.
echo ==============================================
pause
