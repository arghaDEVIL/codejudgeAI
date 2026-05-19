# 🚀 Deployment Guide - CodeJudge AI

Complete guide to deploy CodeJudge AI to production.

## 📋 Table of Contents
1. [Quick Deploy Options](#quick-deploy-options)
2. [Vercel + Railway (Recommended)](#vercel--railway-recommended)
3. [Vercel + Render](#vercel--render)
4. [Docker Deployment](#docker-deployment)
5. [Manual Deployment](#manual-deployment)
6. [Environment Variables](#environment-variables)
7. [Post-Deployment](#post-deployment)

---

## 🎯 Quick Deploy Options

### Option 1: Vercel (Frontend) + Railway (Backend) ⭐ Recommended
- **Frontend**: Vercel (Free tier available)
- **Backend**: Railway (Free $5 credit/month)
- **Database**: Railway PostgreSQL (Included)
- **Setup Time**: ~10 minutes

### Option 2: Vercel (Frontend) + Render (Backend)
- **Frontend**: Vercel (Free tier)
- **Backend**: Render (Free tier with limitations)
- **Database**: Render PostgreSQL (Free tier)
- **Setup Time**: ~15 minutes

### Option 3: Docker + VPS
- **All-in-one**: Docker Compose
- **Server**: Any VPS (DigitalOcean, AWS, etc.)
- **Setup Time**: ~30 minutes

---

## 🚂 Vercel + Railway (Recommended)

### Step 1: Deploy Backend to Railway

1. **Create Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `codejudgeAI` repository

3. **Add PostgreSQL Database**
   - Click "New" → "Database" → "PostgreSQL"
   - Railway will automatically create the database

4. **Configure Backend Service**
   - Click on your service
   - Go to "Settings" → "Environment"
   - Add these variables:
     ```
     DATABASE_URL=${{Postgres.DATABASE_URL}}
     SECRET_KEY=your-super-secret-key-change-this
     GEMINI_API_KEY=your-gemini-api-key
     DOCKER_ENABLED=false
     ```

5. **Set Build & Start Commands**
   - Go to "Settings" → "Build"
   - Build Command: `cd backend && pip install -r requirements.txt`
   - Start Command: `cd backend && alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT`

6. **Deploy**
   - Railway will automatically deploy
   - Copy your backend URL (e.g., `https://your-app.railway.app`)

### Step 2: Deploy Frontend to Vercel

1. **Create Vercel Account**
   - Go to [vercel.com](https://vercel.com)
   - Sign up with GitHub

2. **Import Project**
   - Click "Add New" → "Project"
   - Import `codejudgeAI` repository

3. **Configure Build Settings**
   - Framework Preset: Vite
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`

4. **Add Environment Variables**
   ```
   VITE_API_URL=https://your-backend.railway.app
   ```

5. **Deploy**
   - Click "Deploy"
   - Your frontend will be live at `https://your-app.vercel.app`

### Step 3: Update CORS Settings

1. **Update Backend CORS**
   - In Railway, add environment variable:
     ```
     CORS_ORIGINS=https://your-app.vercel.app
     ```

2. **Redeploy Backend**
   - Railway will automatically redeploy

---

## 🎨 Vercel + Render

### Step 1: Deploy Backend to Render

1. **Create Render Account**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub

2. **Create PostgreSQL Database**
   - Click "New" → "PostgreSQL"
   - Name: `codejudge-db`
   - Plan: Free
   - Copy the Internal Database URL

3. **Create Web Service**
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Name: `codejudge-backend`
   - Environment: Python 3
   - Build Command: `cd backend && pip install -r requirements.txt`
   - Start Command: `cd backend && alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Add Environment Variables**
   ```
   DATABASE_URL=<your-postgres-internal-url>
   SECRET_KEY=your-super-secret-key
   GEMINI_API_KEY=your-gemini-api-key
   DOCKER_ENABLED=false
   PYTHON_VERSION=3.9.0
   ```

5. **Deploy**
   - Render will build and deploy
   - Copy your backend URL

### Step 2: Deploy Frontend to Vercel

Follow the same steps as in Railway + Vercel option above.

---

## 🐳 Docker Deployment

### Prerequisites
- Docker and Docker Compose installed
- VPS with at least 2GB RAM

### Step 1: Clone Repository on Server

```bash
git clone https://github.com/arghaDEVIL/codejudgeAI.git
cd codejudgeAI
```

### Step 2: Configure Environment

```bash
# Create .env file
cat > backend/.env << EOF
DATABASE_URL=postgresql://codejudge:codejudge123@postgres:5432/codejudge
SECRET_KEY=$(openssl rand -hex 32)
GEMINI_API_KEY=your-gemini-api-key
DOCKER_ENABLED=false
EOF
```

### Step 3: Build and Run

```bash
# Build and start all services
docker-compose up -d

# Check logs
docker-compose logs -f

# Run migrations
docker-compose exec backend alembic upgrade head

# Add sample problems
docker-compose exec backend python add_curated_problems.py
```

### Step 4: Configure Nginx (Optional)

```nginx
# /etc/nginx/sites-available/codejudge
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        proxy_pass http://localhost:5173;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # WebSocket
    location /ws {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
        proxy_set_header Host $host;
    }
}
```

---

## 🔧 Environment Variables

### Backend Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:5432/db` |
| `SECRET_KEY` | JWT secret key | `your-secret-key-min-32-chars` |
| `GEMINI_API_KEY` | Google Gemini API key | `AIza...` |

### Backend Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DOCKER_ENABLED` | Enable Docker code execution | `false` |
| `CORS_ORIGINS` | Allowed CORS origins | `*` |
| `MAX_CODE_LENGTH` | Max code length in chars | `10000` |
| `CODE_TIMEOUT` | Code execution timeout (seconds) | `10` |

### Frontend Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `VITE_API_URL` | Backend API URL | `https://api.yourapp.com` |

---

## 📝 Post-Deployment Checklist

### 1. Database Setup
```bash
# Run migrations
alembic upgrade head

# Add sample problems
python backend/add_curated_problems.py

# Add test cases
python backend/add_testcases.py
```

### 2. Create Admin User
```bash
# Access your backend
curl -X POST https://your-backend.com/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Admin",
    "email": "admin@example.com",
    "password": "admin123"
  }'
```

### 3. Test Endpoints
```bash
# Health check
curl https://your-backend.com/health

# Get problems
curl https://your-backend.com/api/v1/problems/

# Test WebSocket
wscat -c wss://your-backend.com/ws
```

### 4. Configure Domain (Optional)
- Add custom domain in Vercel/Railway
- Update DNS records
- Enable HTTPS (automatic on Vercel/Railway)

### 5. Monitor Application
- Check Railway/Render logs
- Monitor database usage
- Set up error tracking (Sentry)

---

## 🔒 Security Checklist

- [ ] Change default SECRET_KEY
- [ ] Use strong database password
- [ ] Enable HTTPS
- [ ] Configure CORS properly
- [ ] Set up rate limiting
- [ ] Enable database backups
- [ ] Use environment variables for secrets
- [ ] Disable DEBUG mode in production

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check logs
railway logs  # or render logs

# Common issues:
# 1. Missing environment variables
# 2. Database connection failed
# 3. Migration errors
```

### Frontend can't connect to backend
```bash
# Check CORS settings
# Verify VITE_API_URL is correct
# Check browser console for errors
```

### Database connection errors
```bash
# Verify DATABASE_URL format
# Check database is running
# Verify network connectivity
```

### WebSocket connection fails
```bash
# Check WebSocket URL (ws:// or wss://)
# Verify backend supports WebSocket
# Check firewall/proxy settings
```

---

## 📊 Monitoring & Maintenance

### Railway
- Dashboard: Monitor CPU, Memory, Network
- Logs: Real-time application logs
- Metrics: Request count, response time

### Render
- Dashboard: Service health, metrics
- Logs: Application and build logs
- Alerts: Set up email notifications

### Database Backups
```bash
# Railway: Automatic daily backups
# Render: Manual backups in dashboard
# Docker: Use pg_dump
pg_dump -U codejudge codejudge > backup.sql
```

---

## 🚀 Scaling

### Horizontal Scaling
- Railway: Increase replicas in dashboard
- Render: Upgrade to paid plan for scaling
- Docker: Use Docker Swarm or Kubernetes

### Vertical Scaling
- Railway: Upgrade plan for more resources
- Render: Upgrade instance type
- VPS: Resize server

### Database Scaling
- Add read replicas
- Enable connection pooling
- Optimize queries
- Add indexes

---

## 💰 Cost Estimation

### Free Tier (Hobby Projects)
- **Vercel**: Free (100GB bandwidth)
- **Railway**: $5 credit/month (enough for small apps)
- **Render**: Free (with limitations)
- **Total**: $0-5/month

### Production (Small Scale)
- **Vercel Pro**: $20/month
- **Railway Pro**: $20/month
- **Database**: Included
- **Total**: ~$40/month

### Production (Medium Scale)
- **Vercel Pro**: $20/month
- **Railway**: $50/month
- **Dedicated Database**: $25/month
- **Total**: ~$95/month

---

## 📚 Additional Resources

- [Railway Documentation](https://docs.railway.app)
- [Render Documentation](https://render.com/docs)
- [Vercel Documentation](https://vercel.com/docs)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Vite Deployment](https://vitejs.dev/guide/static-deploy.html)

---

## 🆘 Support

If you encounter issues:
1. Check the troubleshooting section
2. Review application logs
3. Open an issue on GitHub
4. Join our Discord community

---

## ✅ Deployment Complete!

Your CodeJudge AI platform is now live! 🎉

**Next Steps:**
1. Share your app URL
2. Add custom domain
3. Monitor performance
4. Gather user feedback
5. Iterate and improve

---

Made with ❤️ by arghaDEVIL
