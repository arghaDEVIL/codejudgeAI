# 🚀 Complete Setup Guide

## Step-by-Step Installation

### 1. Database Setup

#### Install PostgreSQL
**Windows:**
- Download from https://www.postgresql.org/download/windows/
- Run installer and remember your password

**Mac:**
```bash
brew install postgresql@16
brew services start postgresql@16
```

**Linux:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

#### Create Database
```bash
# Access PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE codejudge;

# Exit
\q
```

### 2. Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env with your settings
# Update DATABASE_URL with your PostgreSQL password
# Generate SECRET_KEY: openssl rand -hex 32

# Run the server
python run.py
```

The backend will start on `http://localhost:8000`

Visit `http://localhost:8000/docs` to see the API documentation.

### 3. Frontend Setup

```bash
# Open new terminal
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

The frontend will start on `http://localhost:5173`

### 4. Test the Application

1. Open `http://localhost:5173`
2. Click "Create Account"
3. Register a new user
4. Login with your credentials
5. You'll be redirected to the Judge page

### 5. Add Sample Problems

You can add problems via the API:

```bash
curl -X POST "http://localhost:8000/api/v1/problems" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Two Sum",
    "statement": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
    "difficulty": "Easy",
    "expected_output": "0 1"
  }'
```

Or use the Swagger UI at `http://localhost:8000/docs`

## Common Issues

### Issue: Database Connection Error
**Solution:** Check your DATABASE_URL in `.env` file. Make sure PostgreSQL is running.

### Issue: Port Already in Use
**Solution:** 
```bash
# Kill process on port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux:
lsof -ti:8000 | xargs kill -9
```

### Issue: Module Not Found
**Solution:** Make sure virtual environment is activated and dependencies are installed.

### Issue: CORS Error
**Solution:** Check that FRONTEND_URL in backend `.env` matches your frontend URL.

## Development Workflow

### Backend Development
```bash
cd backend
source venv/bin/activate  # Activate venv
python run.py  # Run with auto-reload
```

### Frontend Development
```bash
cd frontend
npm run dev  # Run with hot reload
```

### Database Migrations
When you change models:
```bash
# The app automatically creates tables on startup
# For production, use Alembic for migrations
```

## Next Steps

1. ✅ Test user registration and login
2. ✅ Add sample problems via API
3. ✅ Test code submission
4. 📖 Read the main README.md for features
5. 🚀 Start building new features!

## Useful Commands

### Backend
```bash
# Run server
python run.py

# Run with specific host/port
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Check database
psql -U postgres -d codejudge
```

### Frontend
```bash
# Development
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

## Environment Variables Reference

### Backend (.env)
```env
# Database
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/codejudge

# JWT (Generate with: openssl rand -hex 32)
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
FRONTEND_URL=http://localhost:5173

# App
DEBUG=True
```

## Architecture Overview

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   React     │────────▶│   FastAPI   │────────▶│ PostgreSQL  │
│  Frontend   │  HTTP   │   Backend   │  SQL    │  Database   │
│  (Port 5173)│◀────────│ (Port 8000) │◀────────│             │
└─────────────┘   JSON  └─────────────┘  Data   └─────────────┘
      │                        │
      │                        │
      ▼                        ▼
  JWT Token              Code Execution
  Management             (subprocess)
```

## Security Checklist

- [x] JWT authentication implemented
- [x] Password hashing with bcrypt
- [x] Protected API routes
- [x] CORS configured
- [x] Input validation
- [ ] Rate limiting (TODO)
- [ ] Docker sandbox (TODO)

## Performance Tips

1. **Database Indexing**: Already added on email, user_id, problem_id
2. **Connection Pooling**: Configured in SQLAlchemy
3. **Frontend Optimization**: Use React.memo for expensive components
4. **API Caching**: Consider Redis for frequently accessed data

## Troubleshooting

### Backend won't start
1. Check if PostgreSQL is running
2. Verify DATABASE_URL in .env
3. Check if port 8000 is available
4. Ensure all dependencies are installed

### Frontend won't start
1. Delete node_modules and package-lock.json
2. Run `npm install` again
3. Check if port 5173 is available
4. Clear browser cache

### Code execution fails
1. Ensure Python is in PATH
2. For C++: Install g++ compiler
3. Check file permissions in temp directory

## Getting Help

- Check the main README.md
- Review API docs at /docs
- Check console for errors
- Review logs in terminal

Happy Coding! 🎉
