@echo off
echo ========================================
echo  PUSH CACHE FIX TO MAIN BRANCH
echo ========================================
echo.

echo You're on 'all-features-final' branch but Render needs 'main'
echo.

echo Step 1: Check current branch...
git branch

echo Step 2: Push current branch to GitHub...
git push origin all-features-final

echo Step 3: Switch to main branch...
git checkout main

echo Step 4: Merge the fix from all-features-final...
git merge all-features-final

echo Step 5: Push to main (this will trigger Render deployment)...
git push origin main

echo.
echo ========================================
echo  DEPLOYMENT TRIGGERED ON MAIN!
echo ========================================
echo.
echo Now Render should:
echo ✅ Detect the new commit on main branch
echo ✅ Start fresh deployment with cache fix
echo ✅ Run migration 0006 (no operations - can't fail)
echo ✅ Deploy successfully with all your features
echo.
echo Check your Render dashboard for the deployment!
echo.
pause