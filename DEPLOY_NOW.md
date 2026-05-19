# 🚀 Deploy CodeJudge AI in 10 Minutes

## Quick Deploy - Railway + Vercel (Recommended)

### 🎯 What You'll Get
- ✅ Live backend API on Railway
- ✅ Live frontend on Vercel
- ✅ PostgreSQL database (free)
- ✅ HTTPS enabled automatically
- ✅ Auto-deploy on git push

---

## Step 1: Deploy Backend (5 minutes)

### Railway Deployment

1. **Go to Railway**
   - Visit: https://railway.app
   - Click "Start a New Project"
   - Login with GitHub

2. **Deploy from GitHub**
   - Click "Deploy from GitHub repo"
   - Select `arghaDEVIL/codejudgeAI`
   - Railway will detect it's a Python app

3. **Add PostgreSQL**
   - Click "New" → "Database" → "PostgreSQL"
   - Database will be created automatically

4. **Configure Environment Variables**
   - Click on your service → "Variables"
   - Add these:
   ```
   DATABASE_URL=${{Postgres.DATABASE_URL}}
   SECRET_KEY=change-this-to-a-random-32-char-string
   GEMINI_API_KEY=your-gemini-api-key-here
   DOCKER_ENABLED=false
   ```

5. **Set Commands**
   - Go to "Settings"
   - Build Command: `cd backend && pip install -r requirements.txt`
   - Start Command: `cd backend && alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT`

6. **Deploy!**
   - Railway will automatically build and deploy
   - Copy your backend URL: `https://your-app.up.railway.app`

---

## Step 2: Deploy Frontend (5 minutes)

### Vercel Deployment

1. **Go to Vercel**
   - Visit: https://vercel.com
   - Click "Add New" → "Project"
   - Login with GitHub

2. **Import Repository**
   - Select `arghaDEVIL/codejudgeAI`
   - Click "Import"

3. **Configure Project**
   - Framework Preset: **Vite**
   - Root Directory: **frontend**
   - Build Command: `npm run build`
   - Output Directory: `dist`

4. **Add Environment Variable**
   ```
   VITE_API_URL=https://your-backend.up.railway.app
   ```
   (Use the URL from Step 1)

5. **Deploy!**
   - Click "Deploy"
   - Wait 2-3 minutes
   - Your app is live! 🎉

---

## Step 3: Initialize Database (2 minutes)

### Add Sample Problems

1. **Open Railway Dashboard**
   - Go to your backend service
   - Click "Deploy Logs"

2. **Run Setup Commands**
   - The migrations run automatically on deploy
   - Problems will be added on first run

**OR manually via Railway CLI:**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link project
railway link

# Run commands
railway run python backend/add_curated_problems.py
railway run python backend/add_testcases.py
```

---

## Step 4: Test Your Deployment ✅

1. **Visit Your Frontend**
   - Go to: `https://your-app.vercel.app`
   - You should see the login page

2. **Register an Account**
   - Click "Register"
   - Create your account

3. **Test the Judge**
   - Go to Judge page
   - Select a problem
   - Write code and submit!

---

## 🎉 You're Live!

Your CodeJudge AI is now deployed and accessible worldwide!

### Your URLs:
- **Frontend**: `https://your-app.vercel.app`
- **Backend API**: `https://your-backend.up.railway.app`
- **API Docs**: `https://your-backend.up.railway.app/docs`

---

## 🔧 Post-Deployment

### Update CORS (Important!)

1. **Go to Railway**
   - Click on your backend service
   - Go to "Variables"
   - Add:
   ```
   CORS_ORIGINS=https://your-app.vercel.app
   ```

2. **Redeploy**
   - Railway will automatically redeploy
   - CORS will be configured

### Add Custom Domain (Optional)

**Vercel:**
1. Go to Project Settings → Domains
2. Add your domain
3. Update DNS records as shown

**Railway:**
1. Go to Settings → Domains
2. Add custom domain
3. Update DNS records

---

## 📊 Monitor Your App

### Railway Dashboard
- **Metrics**: CPU, Memory, Network usage
- **Logs**: Real-time application logs
- **Database**: Connection stats, storage

### Vercel Dashboard
- **Analytics**: Page views, performance
- **Logs**: Build and runtime logs
- **Deployments**: History and rollback

---

## 🐛 Troubleshooting

### Frontend can't connect to backend
```
Error: Network Error or CORS Error
```
**Solution**: Add CORS_ORIGINS environment variable in Railway

### Backend deployment failed
```
Error: Build failed
```
**Solution**: Check Railway logs, verify requirements.txt

### Database connection error
```
Error: Could not connect to database
```
**Solution**: Verify DATABASE_URL is set correctly

---

## 💡 Pro Tips

1. **Enable Auto-Deploy**
   - Both Railway and Vercel auto-deploy on git push
   - Just push to main branch!

2. **Monitor Costs**
   - Railway: $5 free credit/month
   - Vercel: 100GB bandwidth free
   - Check usage in dashboards

3. **Backup Database**
   - Railway: Automatic daily backups
   - Download backups from dashboard

4. **Scale When Needed**
   - Railway: Upgrade plan for more resources
   - Vercel: Automatic scaling

---

## 🚀 Next Steps

1. **Share Your App**
   - Share the Vercel URL with friends
   - Get feedback

2. **Add More Problems**
   - Use the admin panel
   - Import from problem importers

3. **Customize**
   - Update branding
   - Add your own features

4. **Monitor & Improve**
   - Check analytics
   - Fix bugs
   - Add features

---

## 📚 Need Help?

- **Full Guide**: See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- **Railway Docs**: https://docs.railway.app
- **Vercel Docs**: https://vercel.com/docs
- **GitHub Issues**: Open an issue if stuck

---

## ✅ Deployment Checklist

- [ ] Backend deployed on Railway
- [ ] PostgreSQL database created
- [ ] Environment variables configured
- [ ] Frontend deployed on Vercel
- [ ] CORS configured
- [ ] Database initialized
- [ ] Sample problems added
- [ ] Test account created
- [ ] Code submission tested
- [ ] WebSocket tested (rooms)

---

**Congratulations! Your CodeJudge AI is live! 🎉**

Share it with the world: `https://your-app.vercel.app`

---

Made with ❤️ by arghaDEVIL
