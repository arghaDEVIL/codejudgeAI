# 🚀 AI Code Judge Platform

A modern, full-stack competitive programming platform similar to LeetCode/Codeforces, featuring real-time code execution, JWT authentication, and a beautiful UI.

![Tech Stack](https://img.shields.io/badge/React-19.2-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)
![Python](https://img.shields.io/badge/Python-3.11+-yellow)

## ✨ Features

### Current Features
- ✅ **User Authentication** - JWT-based secure authentication
- ✅ **Protected Routes** - Frontend and backend route protection
- ✅ **Multi-Language Support** - Python and C++ code execution
- ✅ **Real-time Code Editor** - Monaco Editor integration
- ✅ **Problem Management** - Browse and solve coding problems
- ✅ **Submission System** - Track all code submissions
- ✅ **Verdict System** - Accepted, Wrong Answer, Runtime Error, TLE, Compilation Error
- ✅ **Modern UI** - Glassmorphism design with Tailwind CSS
- ✅ **Responsive Design** - Works on all devices

### Coming Soon
- 🔄 Testcase System (multiple test cases with stdin support)
- 🔄 Hidden vs Sample Testcases
- 🔄 Leaderboard & Rankings
- 🔄 User Profiles & Statistics
- 🔄 Problem Tags & Filtering
- 🔄 AI-Powered Feedback
- 🔄 Docker Sandbox Execution
- 🔄 Contest Mode

## 🏗️ Architecture

```
ai-code-judge/
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── api/               # API routes
│   │   │   └── v1/
│   │   │       ├── endpoints/ # Auth, Problems, Submissions
│   │   │       └── router.py
│   │   ├── core/              # Core configuration
│   │   │   ├── config.py      # Settings management
│   │   │   └── security.py    # JWT & password hashing
│   │   ├── db/                # Database
│   │   │   └── database.py    # SQLAlchemy setup
│   │   ├── models/            # SQLAlchemy models
│   │   │   ├── user.py
│   │   │   ├── problem.py
│   │   │   └── submission.py
│   │   ├── schemas/           # Pydantic schemas
│   │   │   ├── user.py
│   │   │   ├── problem.py
│   │   │   └── submission.py
│   │   └── main.py            # FastAPI app
│   ├── .env                   # Environment variables
│   ├── requirements.txt       # Python dependencies
│   └── run.py                 # Development server
│
├── frontend/                  # React Frontend
│   ├── src/
│   │   ├── utils/
│   │   │   └── api.js         # API client with JWT
│   │   ├── App.jsx            # Main app with routing
│   │   ├── Login.jsx          # Login page
│   │   ├── Register.jsx       # Registration page
│   │   └── Judge.jsx          # Main judge interface
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM for database operations
- **PostgreSQL** - Relational database
- **JWT** - Secure authentication
- **Pydantic** - Data validation
- **Passlib** - Password hashing

### Frontend
- **React 19** - UI library
- **Vite** - Build tool
- **Tailwind CSS** - Utility-first CSS
- **Monaco Editor** - VS Code editor
- **Axios** - HTTP client
- **React Router** - Client-side routing

## 📦 Installation

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- g++ compiler (for C++ support)

### Backend Setup

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd ai-code-judge/backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your database credentials and secret key
```

5. **Create database**
```bash
createdb codejudge  # Or use pgAdmin
```

6. **Run the server**
```bash
python run.py
```

Backend will run on `http://localhost:8000`
API docs available at `http://localhost:8000/docs`

### Frontend Setup

1. **Navigate to frontend**
```bash
cd ../frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Run development server**
```bash
npm run dev
```

Frontend will run on `http://localhost:5173`

## 🔐 Environment Variables

### Backend (.env)
```env
DATABASE_URL=postgresql+psycopg://postgres:password@localhost:5432/codejudge
SECRET_KEY=your-secret-key-here-use-openssl-rand-hex-32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
FRONTEND_URL=http://localhost:5173
DEBUG=True
```

## 📚 API Documentation

### Authentication Endpoints

#### POST `/api/v1/auth/signup`
Register a new user
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "password123"
}
```

#### POST `/api/v1/auth/login`
Login and get JWT token
```json
{
  "email": "john@example.com",
  "password": "password123"
}
```

Response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com"
  }
}
```

#### GET `/api/v1/auth/me`
Get current user (requires authentication)

### Problems Endpoints

#### GET `/api/v1/problems`
Get all problems

#### GET `/api/v1/problems/{id}`
Get specific problem

#### POST `/api/v1/problems`
Create new problem (requires authentication)

### Submissions Endpoints

#### POST `/api/v1/submissions`
Submit code (requires authentication)
```json
{
  "problem_id": 1,
  "code": "print('Hello World')",
  "language": "python"
}
```

#### GET `/api/v1/submissions`
Get user's submissions (requires authentication)

## 🎨 UI Features

- **Glassmorphism Design** - Modern frosted glass effect
- **Gradient Backgrounds** - Beautiful color transitions
- **Smooth Animations** - Hover effects and transitions
- **Dark Theme** - Easy on the eyes
- **Responsive Layout** - Mobile-friendly
- **Icon Integration** - SVG icons throughout
- **Loading States** - Visual feedback for async operations

## 🔒 Security Features

- JWT token-based authentication
- Password hashing with bcrypt
- Protected API routes
- CORS configuration
- SQL injection prevention (SQLAlchemy ORM)
- Input validation (Pydantic)

## 🚀 Deployment

### Backend Deployment (Railway/Render)
1. Set environment variables
2. Use `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
3. Configure PostgreSQL database

### Frontend Deployment (Vercel/Netlify)
1. Build: `npm run build`
2. Deploy `dist` folder
3. Configure environment variables

## 📈 Future Enhancements

### Phase 2: Core Features
- [ ] Multiple testcases with stdin support
- [ ] Hidden vs sample testcases
- [ ] Submission history dashboard
- [ ] Problem difficulty ratings

### Phase 3: Advanced Features
- [ ] Leaderboard system
- [ ] User profiles with statistics
- [ ] Problem tags and categories
- [ ] Search and filter problems
- [ ] Contest mode

### Phase 4: AI Integration
- [ ] AI-powered code feedback
- [ ] Optimization suggestions
- [ ] Code quality analysis
- [ ] Hint system

### Phase 5: Production Ready
- [ ] Docker sandbox for code execution
- [ ] Rate limiting
- [ ] Caching (Redis)
- [ ] Monitoring and logging
- [ ] CI/CD pipeline
- [ ] Comprehensive testing

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License.

## 👨‍💻 Author

Built with ❤️ for competitive programming enthusiasts

---

**Note**: This is a portfolio project showcasing full-stack development skills with modern technologies.
