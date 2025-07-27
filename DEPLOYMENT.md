# Deploying GWAS SNP Search to Render

## Prerequisites
- GitHub account
- Render account (free)

## Step-by-Step Deployment

### 1. Push Your Code to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

### 2. Create Render Account
1. Go to [render.com](https://render.com)
2. Click "Get Started for Free"
3. Sign up with GitHub (recommended)

### 3. Deploy on Render
1. **Dashboard**: Click "New +" → "Web Service"
2. **Connect Repository**: 
   - Choose "Connect a repository"
   - Select your GitHub repo
3. **Configure Service**:
   - **Name**: `gwas-snp-search` (or any name you prefer)
   - **Environment**: `Python 3`
   - **Region**: Choose closest to your users
   - **Branch**: `main`
   - **Build Command**: `chmod +x build.sh && ./build.sh`
   - **Start Command**: `gunicorn app:app`
4. **Advanced Settings**:
   - **Plan**: Free
   - **Auto-Deploy**: Yes
5. **Click "Create Web Service"**

### 4. Environment Variables (Optional)
If needed, add these in Render dashboard:
- `PORT`: 10000 (Render sets this automatically)

### 5. Wait for Deployment
- First deployment takes 5-10 minutes (installing Chrome)
- Subsequent deployments are faster

## Important Notes

### Free Tier Limitations:
- **750 hours/month** (enough for 24/7 uptime)
- **512MB RAM** (sufficient for our app)
- **Shared CPU** (good for our use case)

### Chrome Installation:
- The `build.sh` script installs Chrome and ChromeDriver
- This is required for Selenium web scraping
- First deployment takes longer due to Chrome installation

### File Storage:
- Files are stored temporarily on Render
- Consider implementing cleanup for old files
- For production, use cloud storage (AWS S3, etc.)

## Troubleshooting

### Common Issues:
1. **Build fails**: Check build logs in Render dashboard
2. **Chrome not found**: Ensure `build.sh` is executable
3. **Memory issues**: Optimize scraper settings
4. **Timeout errors**: Increase timeout in app.py

### Logs:
- View logs in Render dashboard
- Check "Logs" tab for errors
- Monitor resource usage

## Your App URL
After deployment, your app will be available at:
`https://your-app-name.onrender.com`

## Next Steps
1. Test your deployed app
2. Share the URL with users
3. Monitor usage and performance
4. Consider upgrading to paid plan if needed 