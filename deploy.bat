@echo off
title Crypto AI Dashboard - One-Click Deployment
echo.
echo ========================================
echo    Crypto AI Dashboard Deployer
echo ========================================
echo.

echo Step 1: Pushing to GitHub...
echo.
cd /d "C:\Users\grace\CascadeProjects\crypto-ai-dashboard"

git add .
git commit -m "Auto deploy: %date% %time%"
git push

echo.
echo Step 2: Deployment Instructions...
echo.
echo ========================================
echo    DEPLOYMENT OPTIONS
echo ========================================
echo.
echo 1. RENDER (Recommended - No Email Verification Required)
echo    - Go to: https://render.com/
echo    - Click: New + ^> Web Service
echo    - Connect: Eva1879/crypto-ai-dashboard
echo    - Your app: https://crypto-ai-dashboard.onrender.com
echo.
echo 2. RAILWAY (Alternative - No Email Verification Required)
echo    - Go to: https://railway.app/
echo    - Click: New Project ^> Deploy from GitHub repo
echo    - Connect: Eva1879/crypto-ai-dashboard
echo    - Your app: https://crypto-ai-dashboard.up.railway.app
echo.
echo 3. STREAMLIT (Requires Email Fix)
echo    - Update GitHub email to match Streamlit
echo    - Go to: https://share.streamlit.io/
echo    - Connect: Eva1879/crypto-ai-dashboard
echo    - Your app: https://eva1879-crypto-ai-dashboard.streamlit.app/
echo.
echo ========================================
echo    CURRENT STATUS
echo ========================================
echo.
echo ✅ Code pushed to GitHub
echo ✅ Repository: https://github.com/Eva1879/crypto-ai-dashboard
echo ✅ Ready for deployment
echo.
echo Next steps:
echo 1. Choose deployment platform above
echo 2. Connect your GitHub repository
echo 3. Deploy with app_complete.py as main file
echo.
pause
