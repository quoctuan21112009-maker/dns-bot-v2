# Quickstart Guide for Render.com Deployment

## 📋 Project Structure

Your project is now organized for Render deployment:

```
dns-bot-v2/
├── backend/
│   ├── app/
│   │   ├── api/          # API routes (auth, chat, code, etc.)
│   │   ├── models/       # Database models
│   │   ├── services/     # Business logic
│   │   ├── security/     # JWT & auth
│   │   ├── main.py       # FastAPI app
│   │   ├── config.py     # Configuration
│   │   ├── database.py   # DB setup
│   │   └── websocket.py  # WebSocket handlers
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── requirements.txt
│   ├── .env.example
│   └── build.sh
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── pages/        # Page components
│   │   ├── services/     # API services
│   │   ├── store/        # Zustand stores
│   │   ├── types/        # TypeScript types
│   │   └── styles/       # CSS files
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── package.json
│   └── .env.example
├── docker-compose.yml    # Local development
├── render.yaml          # Render deployment config
├── .gitignore
├── setup.sh / setup.bat  # Local setup scripts
└── DEPLOYMENT.md        # Deployment guide
```

## 🚀 Quick Deployment Steps

### Step 1: GitHub Preparation
```bash
# Initialize git (if not done)
git init
git add .
git commit -m "Initial commit: DNS Bot v2"
git remote add origin https://github.com/your-username/dns-bot-v2.git
git push -u origin main
```

### Step 2: Create Render Account
- Go to https://render.com
- Sign up with GitHub
- Authorize access to your repositories

### Step 3: Deploy via render.yaml (Easiest!)
1. On Render dashboard, click **"New"** → **"Blueprint"**
2. Select your GitHub repository
3. Render auto-detects `render.yaml` 
4. Add environment variables:
   - `SECRET_KEY` - Generate random key
   - `GROQ_API_KEY` - From https://console.groq.com
   - `OPENAI_API_KEY` - From https://platform.openai.com
   - `GEMINI_API_KEY` - From Google AI Studio
   - `GITHUB_API_TOKEN` - From GitHub Settings
   - Other API keys as needed
5. Click **"Create Blueprint"**
6. Wait 5-10 minutes for deployment

### Step 4: Access Your App
- **Frontend**: `https://<your-frontend-name>.render.onrender.com`
- **Backend API**: `https://<your-backend-name>.render.onrender.com`
- **API Docs**: `https://<your-backend-name>.render.onrender.com/docs`

## 💻 Local Development

### Prerequisites
- Docker Desktop installed
- Python 3.11+ (for local backend dev)
- Node.js 18+ (for local frontend dev)

### Run Locally with Docker

**On Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

**On Windows:**
```bash
setup.bat
```

Or manually:
```bash
# Create environment files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# Update backend/.env with your API keys

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Run Locally without Docker

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Set up PostgreSQL and Redis databases
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

## 🔧 Configuration

### Backend Configuration
Edit `backend/app/config.py`:
- Database connection settings
- Security settings
- API provider keys
- File upload limits
- CORS origins

### Environment Variables
Edit `.env` files:

**Backend .env**
```
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/db
REDIS_URL=redis://host:6379/0
GROQ_API_KEY=your_key
OPENAI_API_KEY=your_key
SECRET_KEY=your_secret_key
DEBUG=False
```

**Frontend .env**
```
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
```

## 📦 Building Docker Images Locally

```bash
# Build backend
docker build -t dns-bot-backend ./backend

# Build frontend
docker build -t dns-bot-frontend ./frontend

# Run backend
docker run -p 8000:8000 -e DATABASE_URL="..." dns-bot-backend

# Run frontend
docker run -p 5173:5173 dns-bot-frontend
```

## 🆘 Troubleshooting

### Services won't start
- Check Docker is running: `docker --version`
- Check requirements.txt is updated
- Check environment variables are set

### Frontend can't connect to backend
- Update `VITE_API_URL` in frontend/.env
- Check backend is running on correct port
- Check CORS settings in backend/app/main.py

### Database connection failed
- Verify DATABASE_URL in .env
- Check PostgreSQL is running
- Verify credentials are correct

### View logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
```

## 📝 Important Files for Render

- **render.yaml** - Deployment configuration
- **docker-compose.yml** - Local development setup
- **Dockerfile** (backend & frontend) - Container images
- **requirements.txt** - Python dependencies
- **package.json** - Node.js dependencies
- **.env.example** - Environment template

## 🚨 Before Deploying

- [ ] Update all `.env` files with real API keys
- [ ] Set `DEBUG=False` in production
- [ ] Generate a strong `SECRET_KEY`
- [ ] Update ALLOWED_ORIGINS in config.py
- [ ] Test locally with Docker
- [ ] Push code to GitHub
- [ ] Create Render services in correct order (database → services)

## 📚 Additional Resources

- [Render Documentation](https://render.com/docs)
- [Docker Guide](https://docs.docker.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev)
- [Vite Guide](https://vitejs.dev/)

## 💬 Support

For issues:
1. Check logs: `docker-compose logs -f` or Render dashboard
2. Review DEPLOYMENT.md for detailed troubleshooting
3. Check API keys are correct
4. Verify network connectivity

---

**Ready to deploy?** Follow the Quick Deployment Steps above and you'll be live in minutes! 🎉
