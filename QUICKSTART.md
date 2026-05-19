# ⚡ Quick Start Guide

Get up and running in 5 minutes!

## Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 14+

## 🚀 Fast Setup

### 1. Database (1 minute)
```bash
# Create database
createdb codejudge
```

### 2. Backend (2 minutes)
```bash
cd backend

# Setup environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env: Update DATABASE_URL password

# Run
python run.py
```

✅ Backend running on http://localhost:8000

### 3. Frontend (2 minutes)
```bash
# New terminal
cd frontend

# Setup and run
npm install
npm run dev
```

✅ Frontend running on http://localhost:5173

## 🎯 Test It

1. Open http://localhost:5173
2. Click "Create Account"
3. Register: name, email, password
4. Login with credentials
5. Start coding! 🎉

## 📚 What's Available

### API Endpoints
- `POST /api/v1/auth/signup` - Register
- `POST /api/v1/auth/login` - Login
- `GET /api/v1/auth/me` - Get user info
- `GET /api/v1/problems` - List problems
- `POST /api/v1/submissions` - Submit code

### API Docs
http://localhost:8000/docs

### Features
- ✅ JWT Authentication
- ✅ Python & C++ Support
- ✅ Monaco Code Editor
- ✅ Real-time Execution
- ✅ Beautiful UI

## 🐛 Quick Fixes

**Port in use?**
```bash
# Kill port 8000
lsof -ti:8000 | xargs kill -9  # Mac/Linux
netstat -ano | findstr :8000   # Windows
```

**Database error?**
- Check PostgreSQL is running
- Verify DATABASE_URL in .env

**Module not found?**
- Activate virtual environment
- Run `pip install -r requirements.txt`

## 📖 Next Steps

- Read [README.md](README.md) for full documentation
- Check [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed setup
- Review [PHASE1_COMPLETE.md](PHASE1_COMPLETE.md) for architecture

## 🎓 Learn More

- **Backend**: FastAPI + PostgreSQL + JWT
- **Frontend**: React + Vite + Tailwind
- **Editor**: Monaco (VS Code editor)
- **Auth**: JWT tokens with bcrypt

Happy Coding! 🚀
