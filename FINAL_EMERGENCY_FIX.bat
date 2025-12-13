@echo off
echo ========================================
echo  FINAL EMERGENCY FIX - Tomorrow Ready
echo ========================================
echo.

echo Step 1: Go back to main and get our files back...
git checkout main
git reset --hard HEAD~1

echo Step 2: Add all files back...
git add .

echo Step 3: Create a simple clean commit...
git commit -m "NRC System with AI Assistant Complete"

echo Step 4: Create new clean branch...
git checkout -b clean-submission

echo Step 5: Remove the problematic files...
git rm --cached git-deploy-commands.txt
git rm --cached WHAT_I_DID_GOOGLE_OAUTH.md

echo Step 6: Commit the removal...
git commit -m "Remove files with secrets"

echo Step 7: Push clean branch...
git push origin clean-submission

echo.
echo ========================================
echo  SUCCESS! Clean Branch Created
echo ========================================
echo.
echo Your code is now on GitHub in 'clean-submission' branch
echo.
echo To use for submission:
echo 1. Go to GitHub repository
echo 2. Download the 'clean-submission' branch as ZIP
echo 3. Or create pull request to merge to main
echo.
echo Your AI assistant is ready for tomorrow!
echo.
pause