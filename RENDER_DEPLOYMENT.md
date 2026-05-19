# 🚀 Deploy to Render - Step by Step Guide

Complete guide to deploy CodeJudge AI backend to Render.

---

## 📋 Prerequisites

- GitHub account with codejudgeAI repository
- Render account (sign up at https://render.com)
- Gemini API key (get from https://ai.google.dev/)

---

## Step 1: Create PostgreSQL Database (3 minutes)

1. **Go to Render Dashboard**
   - Visit: https://dashboard.render.com
   - Click "New +" → "PostgreSQL"

2. **Configure Database**
   - **Name**: `codejudge-db`
   - **Database**: `codejudge`
   - **User**: `codejudge`
   - **Region**: Choose closest to you
   - **Plan**: Free (or paid for production)

3. **Create Database**
   - Click "Create Database"
   - Wait for database to be created (~1 minute)

4. **Copy Connection Strings**
   - **Internal Database URL**: Copy this (starts with `postgresql://`)
   - **External Database URL**: Also copy this
   - Save both URLs - you'll need them!

---

## Step 2: Create Web Service (5 minutes)

1. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Click "Build and deploy from a Git repository"
   - Click "Next"

2. **Connect GitHub Repository**
   - If not connected, click "Connect GitHub"
   - Authorize Render
   - Select `arghaDEVIL/codejudgeAI` repository
   - Click "Connect"

3. **Configure Service**
   Fill in these settings:

   **Basic Settings:**
   - **Name**: `codejudge-backend` (or your choice)
   - **Region**: Same as database
   - **Branch**: `main`
   - **Root Directory**: Leave empty (or `backend` if needed)
   - **Runtime**: `Python 3`

   **Build Settings:**
   - **Build Command**: 
     ```bash
     cd backend && pip install -r requirements.txt
     ```

   - **Start Command**:
     ```bash
     cd backend && alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT
     ```

   **Instance Type:**
   - **Plan**: Free (or paid for production)

4. **Add Environment Variables**
   Click "Advanced" → "Add Environment Variable"

   Add these variables:

   | Key | Value |
   |-----|-------|
   | `DATABASE_URL` | Paste Internal Database URL from Step 1 |
   | `SECRET_KEY` | Generate a random 32+ character string |
   | `GEMINI_API_KEY` | Your Gemini API key |
   | `DOCKER_ENABLED` | `false` |
   | `PYTHON_VERSION` | `3.9.0` |

   **To generate SECRET_KEY:**
   ```bash
   # On Linux/Mac
   openssl rand -hex 32
   
   # Or use this online: https://randomkeygen.com/
   # Choose "CodeIgniter Encryption Keys" (256-bit)
   ```

5. **Create Web Service**
   - Click "Create Web Service"
   - Render will start building your app
   - This takes 5-10 minutes for first deploy

---

## Step 3: Monitor Deployment

1. **Watch Build Logs**
   - You'll see logs in real-time
   - Look for:
     ```
     ==> Installing dependencies
     ==> Building application
     ==> Starting service
     ```

2. **Wait for "Live" Status**
   - Service status will change from "Building" → "Live"
   - You'll see a green "Live" badge

3. **Copy Your Backend URL**
   - At the top, you'll see your URL
   - Example: `https://codejudge-backend.onrender.com`
   - **Save this URL** - you'll need it for frontend!

---

## Step 4: Verify Backend is Working

1. **Test Health Endpoint**
   ```bash
   curl https://your-backend.onrender.com/health
   ```
   Should return: `{"status":"healthy"}`

2. **Test API Docs**
   - Visit: `https://your-backend.onrender.com/docs`
   - You should see FastAPI Swagger UI

3. **Test Problems Endpoint**
   ```bash
   curl https://your-backend.onrender.com/api/v1/problems/
   ```
   Should return JSON array of problems

---

## Step 5: Initialize Database

### Option A: Using Render Shell (Recommended)

1. **Open Shell**
   - In Render dashboard, click on your service
   - Click "Shell" tab
   - Click "Launch Shell"

2. **Run Setup Commands**
   ```bash
   cd backend
   
   # Add sample problems
   python add_curated_problems.py
   
   # Add test cases
   python add_testcases.py
   
   # Verify
   python -c "from app.db.database import SessionLocal; from app.models.problem import Problem; db = SessionLocal(); print(f'Problems: {db.query(Problem).count()}'); db.close()"
   ```

### Option B: Using API (Alternative)

If shell doesn't work, you can add problems via API after deploying frontend.

---

## Step 6: Configure CORS

1. **Add CORS Environment Variable**
   - Go to "Environment" tab
   - Click "Add Environment Variable"
   - Key: `CORS_ORIGINS`
   - Value: `https://your-frontend.vercel.app` (add after deploying frontend)

2. **Redeploy**
   - Click "Manual Deploy" → "Deploy latest commit"
   - Or it will auto-deploy

---

## Step 7: Deploy Frontend to Vercel

Now that backend is ready, deploy frontend:

1. **Go to Vercel**
   - Visit: https://vercel.com
   - Click "Add New" → "Project"

2. **Import Repository**
   - Select `arghaDEVIL/codejudgeAI`
   - Click "Import"

3. **Configure Build**
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

4. **Add Environment Variable**
   - Key: `VITE_API_URL`
   - Value: `https://your-backend.onrender.com` (from Step 3)

5. **Deploy**
   - Click "Deploy"
   - Wait 2-3 minutes
   - Your frontend is live!

---

## Step 8: Update CORS (Important!)

1. **Go back to Render**
   - Open your backend service
   - Go to "Environment" tab

2. **Update CORS_ORIGINS**
   - Find `CORS_ORIGINS` variable
   - Update value to: `https://your-app.vercel.app`
   - Click "Save Changes"

3. **Service will auto-redeploy**

---

## ✅ Deployment Complete!

Your app is now live:
- **Frontend**: `https://your-app.vercel.app`
- **Backend**: `https://your-backend.onrender.com`
- **API Docs**: `https://your-backend.onrender.com/docs`

---

## 🧪 Test Your Deployment

1. **Visit Frontend**
   - Go to your Vercel URL
   - You should see the login page

2. **Register Account**
   - Click "Register"
   - Create your account
   - Should redirect to dashboard

3. **Test Judge**
   - Go to Judge page
   - Select a problem
   - Write code and submit
   - Should see results!

4. **Test Collaboration**
   - Go to Rooms
   - Create a room
   - Test real-time features

---

## 🔧 Render Configuration Files

Your repository already has `render.yaml` which Render can use:

```yaml
services:
  - type: web
    name: codejudge-backend
    env: python
    buildCommand: cd backend && pip install -r requirements.txt
    startCommand: cd backend && alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: codejudge-db
          property: connectionString
```

---

## 📊 Monitoring

### Render Dashboard

1. **Metrics Tab**
   - CPU usage
   - Memory usage
   - Request count
   - Response time

2. **Logs Tab**
   - Real-time application logs
   - Error tracking
   - Request logs

3. **Events Tab**
   - Deployment history
   - Service events
   - Errors and warnings

### Set Up Alerts

1. **Go to Settings**
2. **Notifications**
3. **Add email for alerts**
4. **Configure alert thresholds**

---

## 🐛 Troubleshooting

### Build Failed

**Error**: `ModuleNotFoundError` or `ImportError`
```
Solution:
1. Check requirements.txt is complete
2. Verify Python version (3.9.0)
3. Check build logs for specific error
```

### Service Won't Start

**Error**: `Application startup failed`
```
Solution:
1. Check DATABASE_URL is correct
2. Verify all environment variables are set
3. Check start command is correct
4. Review logs for specific error
```

### Database Connection Error

**Error**: `could not connect to server`
```
Solution:
1. Use Internal Database URL (not External)
2. Verify database is in same region
3. Check database is running
4. Verify DATABASE_URL format
```

### CORS Error in Frontend

**Error**: `Access-Control-Allow-Origin`
```
Solution:
1. Add CORS_ORIGINS environment variable
2. Set to your Vercel URL
3. Redeploy backend
4. Clear browser cache
```

### Migrations Failed

**Error**: `alembic.util.exc.CommandError`
```
Solution:
1. Check DATABASE_URL is correct
2. Verify database is accessible
3. Run migrations manually in shell
4. Check alembic.ini configuration
```

---

## 💰 Render Pricing

### Free Tier
- **Web Services**: Free (with limitations)
  - Spins down after 15 minutes of inactivity
  - Spins up on first request (cold start ~30 seconds)
  - 750 hours/month free

- **PostgreSQL**: Free
  - 1GB storage
  - Expires after 90 days
  - Good for testing

### Paid Plans
- **Starter**: $7/month
  - Always on (no cold starts)
  - Better performance

- **Standard**: $25/month
  - More resources
  - Better for production

- **PostgreSQL**: $7/month
  - 10GB storage
  - No expiration
  - Automatic backups

---

## 🚀 Performance Tips

1. **Upgrade to Paid Plan**
   - Eliminates cold starts
   - Better performance
   - More reliable

2. **Enable Persistent Disk**
   - For file uploads
   - For caching

3. **Use Connection Pooling**
   - Already configured in SQLAlchemy
   - Improves database performance

4. **Monitor Resource Usage**
   - Check metrics regularly
   - Upgrade if needed

---

## 🔒 Security Checklist

- [ ] Changed SECRET_KEY from default
- [ ] Using strong database password
- [ ] CORS configured properly
- [ ] HTTPS enabled (automatic on Render)
- [ ] Environment variables secured
- [ ] Database backups enabled (paid plan)
- [ ] Monitoring and alerts set up

---

## 📚 Additional Resources

- **Render Docs**: https://render.com/docs
- **Render Status**: https://status.render.com
- **Render Community**: https://community.render.com
- **FastAPI Deployment**: https://fastapi.tiangolo.com/deployment/

---

## 🆘 Need Help?

1. **Check Render Logs**
   - Most issues show up in logs
   - Look for error messages

2. **Render Community**
   - Search for similar issues
   - Ask questions

3. **GitHub Issues**
   - Open an issue on the repository
   - Include error logs

4. **Render Support**
   - Email: support@render.com
   - Response time: 24-48 hours

---

## ✅ Post-Deployment Checklist

- [ ] Backend deployed and live
- [ ] Database created and connected
- [ ] Environment variables configured
- [ ] Migrations run successfully
- [ ] Sample problems added
- [ ] Frontend deployed to Vercel
- [ ] CORS configured
- [ ] Test account created
- [ ] Code submission tested
- [ ] WebSocket tested
- [ ] Monitoring set up
- [ ] Backups configured (if paid)

---

**Congratulations! Your CodeJudge AI is live on Render! 🎉**

Backend URL: `https://your-backend.onrender.com`

---

Made with ❤️ by arghaDEVIL
