# 🏗️ System Architecture

## High-Level Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                             │
│                     http://localhost:5173                        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ HTTP/JSON + JWT
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                      REACT FRONTEND                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Login.jsx  │  │ Register.jsx │  │  Judge.jsx   │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              utils/api.js (API Client)                    │  │
│  │  - JWT Token Management                                   │  │
│  │  - Request/Response Interceptors                          │  │
│  │  - Automatic Auth Header Injection                        │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ REST API Calls
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                     FASTAPI BACKEND                              │
│                  http://localhost:8000                           │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    API Router (v1)                        │  │
│  │  /api/v1/auth      /api/v1/problems   /api/v1/submissions│  │
│  └──────────────────────────────────────────────────────────┘  │
│                             │                                    │
│  ┌──────────────────────────▼────────────────────────────────┐ │
│  │                  Middleware Layer                          │ │
│  │  - CORS                                                    │ │
│  │  - JWT Validation                                          │ │
│  │  - Error Handling                                          │ │
│  └────────────────────────────────────────────────────────────┘ │
│                             │                                    │
│  ┌──────────────────────────▼────────────────────────────────┐ │
│  │                  Business Logic                            │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────┐           │ │
│  │  │   Auth   │  │ Problems │  │  Submissions │           │ │
│  │  │ Endpoints│  │Endpoints │  │  Endpoints   │           │ │
│  │  └──────────┘  └──────────┘  └──────────────┘           │ │
│  └────────────────────────────────────────────────────────────┘ │
│                             │                                    │
│  ┌──────────────────────────▼────────────────────────────────┐ │
│  │                  Data Access Layer                         │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────┐           │ │
│  │  │   User   │  │ Problem  │  │  Submission  │           │ │
│  │  │  Model   │  │  Model   │  │    Model     │           │ │
│  │  └──────────┘  └──────────┘  └──────────────┘           │ │
│  │                  (SQLAlchemy ORM)                          │ │
│  └────────────────────────────────────────────────────────────┘ │
│                             │                                    │
│  ┌──────────────────────────▼────────────────────────────────┐ │
│  │                  Code Execution Engine                     │ │
│  │  - Python Interpreter (subprocess)                         │ │
│  │  - C++ Compiler (g++)                                      │ │
│  │  - Timeout Management                                      │ │
│  │  - Output Capture                                          │ │
│  └────────────────────────────────────────────────────────────┘ │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ SQL Queries
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                    POSTGRESQL DATABASE                           │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │    users     │  │   problems   │  │ submissions  │         │
│  ├──────────────┤  ├──────────────┤  ├──────────────┤         │
│  │ id           │  │ id           │  │ id           │         │
│  │ name         │  │ title        │  │ user_id (FK) │         │
│  │ email        │  │ statement    │  │ problem_id   │         │
│  │ password     │  │ difficulty   │  │ code         │         │
│  │ created_at   │  │ created_at   │  │ language     │         │
│  └──────────────┘  └──────────────┘  │ status       │         │
│                                       │ created_at   │         │
│                                       └──────────────┘         │
└─────────────────────────────────────────────────────────────────┘
```

## Request Flow

### 1. User Registration Flow
```
User → Register.jsx → authAPI.signup()
  → POST /api/v1/auth/signup
    → Validate input (Pydantic)
      → Hash password (bcrypt)
        → Save to database
          → Return user data
            → Redirect to login
```

### 2. User Login Flow
```
User → Login.jsx → authAPI.login()
  → POST /api/v1/auth/login
    → Find user by email
      → Verify password
        → Create JWT token
          → Return token + user data
            → Store in localStorage
              → Redirect to Judge page
```

### 3. Code Submission Flow
```
User → Judge.jsx → submissionsAPI.submit()
  → POST /api/v1/submissions (with JWT)
    → Validate JWT token
      → Get current user
        → Validate problem exists
          → Execute code (subprocess)
            → Compare output
              → Save submission
                → Return verdict
                  → Display result
```

### 4. Protected Route Access
```
User → Access /judge
  → Check isAuthenticated()
    → Token exists?
      → Yes: Render Judge.jsx
        → API calls include JWT
          → Backend validates token
            → Return data
      → No: Redirect to /login
```

## Component Architecture

### Frontend Components

```
App.jsx (Router)
├── Login.jsx
│   └── Uses: authAPI.login()
├── Register.jsx
│   └── Uses: authAPI.signup()
└── Judge.jsx
    ├── Uses: problemsAPI.getAll()
    ├── Uses: submissionsAPI.submit()
    └── Monaco Editor
```

### Backend Modules

```
app/
├── main.py (FastAPI app)
├── core/
│   ├── config.py (Settings)
│   └── security.py (JWT, Password)
├── api/v1/
│   ├── router.py (Main router)
│   └── endpoints/
│       ├── auth.py (Signup, Login, Me)
│       ├── problems.py (CRUD)
│       └── submissions.py (Submit, List)
├── models/ (Database tables)
│   ├── user.py
│   ├── problem.py
│   └── submission.py
├── schemas/ (Request/Response)
│   ├── user.py
│   ├── problem.py
│   └── submission.py
└── db/
    └── database.py (SQLAlchemy)
```

## Data Flow Diagram

```
┌──────────┐
│  Client  │
└────┬─────┘
     │
     │ 1. POST /auth/login
     │    {email, password}
     ▼
┌────────────┐
│   FastAPI  │
└────┬───────┘
     │
     │ 2. Verify credentials
     ▼
┌────────────┐
│ PostgreSQL │
└────┬───────┘
     │
     │ 3. User found
     ▼
┌────────────┐
│   FastAPI  │
└────┬───────┘
     │
     │ 4. Generate JWT
     │    {access_token, user}
     ▼
┌──────────┐
│  Client  │ 5. Store token
└────┬─────┘
     │
     │ 6. GET /problems
     │    Authorization: Bearer <token>
     ▼
┌────────────┐
│   FastAPI  │ 7. Validate JWT
└────┬───────┘
     │
     │ 8. Query problems
     ▼
┌────────────┐
│ PostgreSQL │
└────┬───────┘
     │
     │ 9. Return problems
     ▼
┌──────────┐
│  Client  │ 10. Display problems
└──────────┘
```

## Security Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Security Layers                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Layer 1: Transport Security                                │
│  ┌────────────────────────────────────────────────────┐    │
│  │  HTTPS (Production)                                 │    │
│  │  CORS Configuration                                 │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│  Layer 2: Authentication                                    │
│  ┌────────────────────────────────────────────────────┐    │
│  │  JWT Tokens (HS256)                                 │    │
│  │  Token Expiration (30 min)                          │    │
│  │  Bearer Token in Headers                            │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│  Layer 3: Authorization                                     │
│  ┌────────────────────────────────────────────────────┐    │
│  │  Protected Routes                                   │    │
│  │  User Context Validation                            │    │
│  │  Resource Ownership Checks                          │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│  Layer 4: Data Protection                                   │
│  ┌────────────────────────────────────────────────────┐    │
│  │  Password Hashing (bcrypt)                          │    │
│  │  SQL Injection Prevention (ORM)                     │    │
│  │  Input Validation (Pydantic)                        │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│  Layer 5: Execution Security                                │
│  ┌────────────────────────────────────────────────────┐    │
│  │  Timeout Limits (2-5 seconds)                       │    │
│  │  Temporary File Cleanup                             │    │
│  │  Future: Docker Sandbox                             │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## Database Schema

```sql
-- Users Table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP
);

-- Problems Table
CREATE TABLE problems (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) UNIQUE NOT NULL,
    statement TEXT NOT NULL,
    difficulty VARCHAR(20) NOT NULL,
    expected_output TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP
);

-- Submissions Table
CREATE TABLE submissions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    problem_id INTEGER REFERENCES problems(id) ON DELETE CASCADE,
    code TEXT NOT NULL,
    language VARCHAR(20) NOT NULL,
    status VARCHAR(50) DEFAULT 'Pending',
    execution_time INTEGER,
    memory_used INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_submissions_user_id ON submissions(user_id);
CREATE INDEX idx_submissions_problem_id ON submissions(problem_id);
```

## Technology Stack Details

### Frontend Stack
```
React 19.2
├── Vite 8.0 (Build tool)
├── Tailwind CSS 4.2 (Styling)
├── React Router 7.14 (Routing)
├── Axios 1.15 (HTTP client)
└── Monaco Editor 4.7 (Code editor)
```

### Backend Stack
```
FastAPI 0.115
├── Uvicorn (ASGI server)
├── SQLAlchemy 2.0 (ORM)
├── Pydantic 2.10 (Validation)
├── Python-Jose (JWT)
├── Passlib (Password hashing)
└── Psycopg 3.2 (PostgreSQL driver)
```

### Database
```
PostgreSQL 14+
├── ACID compliance
├── Foreign key constraints
├── Indexes for performance
└── Connection pooling
```

## Deployment Architecture (Future)

```
┌─────────────────────────────────────────────────────────────┐
│                         PRODUCTION                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Frontend (Vercel/Netlify)                                  │
│  ┌────────────────────────────────────────────────────┐    │
│  │  React Build (Static Files)                        │    │
│  │  CDN Distribution                                   │    │
│  │  HTTPS                                              │    │
│  └────────────────────────────────────────────────────┘    │
│                          │                                   │
│                          │ API Calls                         │
│                          ▼                                   │
│  Backend (Railway/Render)                                   │
│  ┌────────────────────────────────────────────────────┐    │
│  │  FastAPI (Uvicorn)                                  │    │
│  │  Docker Container                                   │    │
│  │  Auto-scaling                                       │    │
│  └────────────────────────────────────────────────────┘    │
│                          │                                   │
│                          │ SQL                               │
│                          ▼                                   │
│  Database (Railway/Supabase)                                │
│  ┌────────────────────────────────────────────────────┐    │
│  │  PostgreSQL                                         │    │
│  │  Automated Backups                                  │    │
│  │  Connection Pooling                                 │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│  Code Execution (Future)                                    │
│  ┌────────────────────────────────────────────────────┐    │
│  │  Docker Sandbox                                     │    │
│  │  Isolated Containers                                │    │
│  │  Resource Limits                                    │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## Performance Considerations

### Current Optimizations
- ✅ Database connection pooling
- ✅ Indexed columns (email, user_id, problem_id)
- ✅ Efficient SQL queries (ORM)
- ✅ Frontend code splitting (Vite)

### Future Optimizations
- [ ] Redis caching for problems
- [ ] CDN for static assets
- [ ] Database query optimization
- [ ] API response compression
- [ ] Rate limiting
- [ ] Load balancing

---

**Last Updated**: Phase 1 Complete  
**Version**: 1.0.0  
**Status**: Production-Ready Foundation
