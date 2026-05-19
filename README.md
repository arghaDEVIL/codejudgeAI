# 🚀 CodeJudge AI - Online Coding Platform

An advanced online coding platform with AI-powered feedback, real-time collaboration, and comprehensive problem-solving features.

![CodeJudge AI](https://img.shields.io/badge/CodeJudge-AI-blue)
![Python](https://img.shields.io/badge/Python-3.9+-green)
![React](https://img.shields.io/badge/React-18+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-teal)

## ✨ Features

### 🎯 Core Features
- **Online Code Judge** - Submit and test code against multiple test cases
- **Multiple Languages** - Support for Python and C++
- **Real-time Execution** - Instant code execution with Docker isolation
- **AI Feedback** - Get intelligent feedback powered by Google Gemini AI
- **Problem Library** - Curated collection of coding problems with detailed descriptions

### 👥 Collaborative Features
- **Real-time Collaboration** - Code together with multiple users
- **Live Cursors** - See where others are typing in real-time
- **Chat System** - Built-in chat for team communication
- **Code Snapshots** - Save and restore code versions
- **Room Management** - Create and join coding rooms

### 📊 Advanced Features
- **User Dashboard** - Track your progress and statistics
- **Achievement System** - Earn badges and track milestones
- **Submission History** - View all your past submissions with pagination
- **Problem Filtering** - Filter by difficulty, tags, and search
- **Hidden Test Cases** - Comprehensive testing with sample and hidden cases
- **Score System** - Weighted scoring based on test case difficulty

### 🎨 UI/UX Features
- **Modern Design** - Built with shadcn/ui and Tailwind CSS
- **Dark/Light Theme** - Toggle between themes with system preference support
- **Responsive Layout** - Works perfectly on all screen sizes
- **Markdown Support** - Beautiful problem descriptions with syntax highlighting
- **Monaco Editor** - Professional code editor with IntelliSense

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Robust relational database
- **SQLAlchemy** - ORM for database operations
- **Alembic** - Database migrations
- **Docker** - Secure code execution environment
- **WebSockets** - Real-time communication
- **Google Gemini AI** - AI-powered feedback generation

### Frontend
- **React 18** - Modern UI library
- **Vite** - Fast build tool
- **shadcn/ui** - Beautiful component library
- **Tailwind CSS** - Utility-first CSS framework
- **Monaco Editor** - VS Code's editor
- **React Router** - Client-side routing
- **Axios** - HTTP client
- **React Markdown** - Markdown rendering

## 📦 Installation

### Prerequisites
- Python 3.9+
- Node.js 18+
- PostgreSQL 13+
- Docker (for code execution)

### Backend Setup

1. **Clone the repository**
```bash
git clone https://github.com/arghaDEVIL/codejudgeAI.git
cd codejudgeAI/backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your database credentials and API keys
```

5. **Run migrations**
```bash
alembic upgrade head
```

6. **Add sample problems**
```bash
python add_curated_problems.py
python add_testcases.py
```

7. **Start the server**
```bash
uvicorn app.main:app --reload
```

Backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend**
```bash
cd ../frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Start development server**
```bash
npm run dev
```

Frontend will be available at `http://localhost:5173`

## 🚀 Quick Start

1. **Register an account** at `http://localhost:5173/register`
2. **Login** at `http://localhost:5173/login`
3. **Browse problems** on the Judge page
4. **Write your solution** in the Monaco editor
5. **Submit and get instant feedback**
6. **View your dashboard** to track progress

## 📖 Documentation

### Key Documents
- [Architecture Overview](ARCHITECTURE.md)
- [Setup Guide](SETUP_GUIDE.md)
- [Database Migrations](backend/RUN_MIGRATIONS.md)
- [Docker Execution](backend/DOCKER_EXECUTION_GUIDE.md)
- [Collaborative Coding](COLLABORATIVE_CODING_COMPLETE.md)
- [Problem Importer](AUTOMATED_PROBLEM_IMPORTER.md)

### Feature Documentation
- [Dashboard Feature](DASHBOARD_FEATURE.md)
- [Theme System](THEME_FEATURE.md)
- [Pagination System](PAGINATION_IMPLEMENTATION_COMPLETE.md)
- [Problem Tags & Filters](PROBLEM_DIFFICULTY_TAGS_SYSTEM.md)
- [Hidden Test Cases](backend/HIDDEN_TESTCASE_SYSTEM.md)

## 🎯 Usage Examples

### Submitting Code
```python
# Example: Two Sum Problem
def two_sum(nums, target):
    hash_map = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in hash_map:
            return [hash_map[complement], i]
        hash_map[num] = i
    return []
```

### Creating a Collaborative Room
1. Go to Rooms page
2. Click "Create Room"
3. Share room code with teammates
4. Code together in real-time!

### Filtering Problems
- Filter by difficulty: Easy, Medium, Hard
- Filter by tags: arrays, strings, dynamic-programming, etc.
- Search by title or description
- Combine multiple filters

## 🔧 Configuration

### Environment Variables

**Backend (.env)**
```env
DATABASE_URL=postgresql://user:password@localhost/codejudge
SECRET_KEY=your-secret-key-here
GEMINI_API_KEY=your-gemini-api-key
DOCKER_ENABLED=true
```

**Frontend**
```env
VITE_API_URL=http://localhost:8000
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📊 Database Schema

### Core Tables
- **users** - User accounts and authentication
- **problems** - Coding problems with descriptions
- **testcases** - Sample and hidden test cases
- **submissions** - User code submissions
- **testcase_results** - Individual test case results
- **ai_feedback** - AI-generated feedback

### Collaboration Tables
- **rooms** - Collaborative coding rooms
- **room_participants** - Room membership
- **room_sessions** - Active coding sessions
- **room_messages** - Chat messages
- **room_code_snapshots** - Code version history

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**arghaDEVIL**
- GitHub: [@arghaDEVIL](https://github.com/arghaDEVIL)

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [shadcn/ui](https://ui.shadcn.com/) - Beautiful component library
- [Monaco Editor](https://microsoft.github.io/monaco-editor/) - Code editor
- [Google Gemini](https://ai.google.dev/) - AI feedback generation
- [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS

## 📧 Support

For support, email your-email@example.com or open an issue on GitHub.

## 🗺️ Roadmap

- [ ] Add more programming languages (Java, JavaScript, Go)
- [ ] Implement contest mode
- [ ] Add leaderboards
- [ ] Mobile app
- [ ] Video tutorials
- [ ] Code review system
- [ ] Integration with GitHub
- [ ] Advanced analytics

## ⭐ Star History

If you find this project useful, please consider giving it a star!

---

Made with ❤️ by arghaDEVIL
