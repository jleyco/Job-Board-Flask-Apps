# 🚀 Deployment Guide - Render.com

This guide will help you deploy your Job Board Flask app to Render.com for FREE!

---

## 📋 Prerequisites

1. **GitHub Account** (free) - https://github.com
2. **Render Account** (free) - https://render.com
3. **Git installed** on your computer

---

## 🔧 Step 1: Prepare Your Code (Already Done! ✅)

I've already prepared everything:
- ✅ `requirements.txt` - Updated with production dependencies
- ✅ `build.sh` - Build script for Render
- ✅ `render.yaml` - Render configuration
- ✅ `.gitignore` - Git ignore file

---

## 📤 Step 2: Push Your Code to GitHub

### Option A: Using Git Command Line

1. **Open Command Prompt** in your project folder:
   ```bash
   cd c:\Python\desktop_python_files\other_script\mobile\jobs_flask
   ```

2. **Initialize Git** (if not already done):
   ```bash
   git init
   ```

3. **Add all files**:
   ```bash
   git add .
   ```

4. **Commit your code**:
   ```bash
   git commit -m "Initial commit - Job Board Flask App"
   ```

5. **Create a new repository on GitHub**:
   - Go to https://github.com/new
   - Name it: `job-board-flask` (or any name you want)
   - Make it **Public** or **Private**
   - Don't initialize with README, .gitignore, or license
   - Click "Create repository"

6. **Push to GitHub** (replace YOUR_USERNAME with your GitHub username):
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/job-board-flask.git
   git branch -M main
   git push -u origin main
   ```

### Option B: Using GitHub Desktop (Easier!)

1. Download and install **GitHub Desktop**: https://desktop.github.com
2. Click "Add" → "Add existing repository"
3. Select your project folder
4. Click "Publish repository" to GitHub
5. Choose a name and click "Publish"

---

## 🌐 Step 3: Deploy to Render.com

### 3.1 Sign Up for Render

1. Go to https://render.com
2. Click **"Get Started for Free"**
3. Sign up using your **GitHub account** (recommended)

### 3.2 Create a New Web Service

1. After logging in, click **"New +"** → **"Web Service"**

2. **Connect your GitHub repository**:
   - If first time: Click "Connect account" and authorize Render to access GitHub
   - Select your repository: `job-board-flask`

3. **Configure your service**:
   - **Name**: `job-board-flask` (or any name)
   - **Environment**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: Select **"Free"**

4. Click **"Create Web Service"**

### 3.3 Wait for Deployment

- Render will now build and deploy your app
- This takes 2-5 minutes
- You'll see logs showing the build progress
- When you see "Your service is live 🎉", it's ready!

### 3.4 Get Your Live URL

- Render will give you a URL like: `https://job-board-flask.onrender.com`
- Click it to visit your live app!

---

## 🎉 Step 4: Your App is Live!

**Congratulations!** Your job board is now accessible from anywhere!

Share your URL with anyone: `https://YOUR-APP-NAME.onrender.com`

---

## 🔄 Updating Jobs (Running Scrapers)

Since scrapers need to run on your computer (they require local execution), here's how to update jobs:

### Method 1: Run Scrapers Locally, Then Update

1. **Run scrapers on your computer**:
   ```bash
   python run_all_spiders.py
   ```

2. **Commit and push the updated `scraped_jobs.json`**:
   ```bash
   git add scraped_jobs.json
   git commit -m "Update jobs"
   git push
   ```

3. **Render will automatically redeploy** with the new jobs!

### Method 2: Manual Upload (Quick Update)

1. Run scrapers locally
2. Copy the content of `scraped_jobs.json`
3. Use Render Shell (in your service dashboard) to update the file
   - Click "Shell" in your Render dashboard
   - Edit the file manually

---

## ⚙️ Optional: Auto-Deploy on Push

Render automatically redeploys when you push to GitHub!

**Workflow:**
1. Run scrapers locally: `python run_all_spiders.py`
2. Commit changes: `git add . && git commit -m "Update jobs"`
3. Push to GitHub: `git push`
4. Render automatically redeploys (takes 1-2 minutes)
5. Your live site is updated!

---

## 🐛 Troubleshooting

### Build Fails
- Check build logs in Render dashboard
- Make sure all files were pushed to GitHub
- Verify `requirements.txt` is present

### App Doesn't Start
- Check if `scraped_jobs.json` exists (build.sh creates it)
- Look at the logs in Render dashboard

### Scrapers Not Working on Render
- Scrapers need to run on your local machine
- Push the results to GitHub to update the live site

---

## 💰 Costs

**FREE FOREVER** with limitations:
- ✅ 750 hours/month (more than enough)
- ✅ Unlimited bandwidth
- ⚠️ Sleeps after 15 minutes of inactivity (takes 30 seconds to wake up)

**To remove sleep:** Upgrade to paid plan ($7/month)

---

## 🎯 Next Steps

1. **Custom Domain** (Optional):
   - Go to your service settings in Render
   - Add your custom domain
   - Follow DNS configuration instructions

2. **Scheduled Scraping**:
   - Set up a scheduled task on your computer (Windows Task Scheduler)
   - Or use GitHub Actions to run scrapers automatically

3. **Database** (Future improvement):
   - Consider using a database instead of JSON
   - Render offers free PostgreSQL database

---

## 📞 Need Help?

- **Render Docs**: https://render.com/docs
- **Render Community**: https://community.render.com

---

**Good luck! 🚀**
