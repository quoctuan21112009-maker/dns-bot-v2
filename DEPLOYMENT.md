# Deployment Guide for Render.com

## Prerequisites
- Render.com account
- GitHub repository with the project
- Environment variables/API keys ready

## Step 1: Prepare Your Repository

1. Push your code to GitHub (public or private repository)
2. Ensure `.gitignore` is configured properly
3. All environment files have `.example` versions

## Step 2: Deploy on Render.com

### Option A: Using render.yaml (Recommended)

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New" → "Blueprint"
3. Select your GitHub repository
4. Render will detect `render.yaml` and configure services automatically
5. Set environment variables:
   - `GROQ_API_KEY`
   - `OPENAI_API_KEY`
   - `GEMINI_API_KEY`
   - `GITHUB_API_TOKEN`
   - `JUDGE0_API_KEY`
   - `TWILIO_ACCOUNT_SID`
   - `TWILIO_AUTH_TOKEN`
   - `TWILIO_PHONE`
6. Click "Create Blueprint"

### Option B: Manual Setup

#### Create PostgreSQL Database
1. Dashboard → "New" → "PostgreSQL"
2. Name: `dns-bot-db`
3. Region: Choose closest to your users
4. Plan: Starter (free tier)
5. Note the connection string

#### Create Redis Cache
1. Dashboard → "New" → "Redis"
2. Name: `dns-bot-redis`
3. Region: Same as database
4. Plan: Starter (free tier)
5. Note the connection string

#### Deploy Backend
1. Dashboard → "New" → "Web Service"
2. Connect your GitHub repository
3. Configuration:
   - **Name**: dns-bot-backend
   - **Environment**: Docker
   - **Region**: Same as database
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Root Directory**: `backend`

4. Environment Variables:
   ```
   DATABASE_URL=postgresql+asyncpg://user:password@host:5432/dnsbot_db
   REDIS_URL=redis://default:password@host:10000
   DEBUG=False
   LOG_LEVEL=INFO
   SECRET_KEY=<generate-random-key>
   GROQ_API_KEY=<your-key>
   OPENAI_API_KEY=<your-key>
   GEMINI_API_KEY=<your-key>
   GITHUB_API_TOKEN=<your-key>
   JUDGE0_API_KEY=<your-key>
   TWILIO_ACCOUNT_SID=<your-sid>
   TWILIO_AUTH_TOKEN=<your-token>
   TWILIO_PHONE=<your-phone>
   ```

5. Click "Create Web Service"

#### Deploy Frontend
1. Dashboard → "New" → "Web Service"
2. Connect your GitHub repository
3. Configuration:
   - **Name**: dns-bot-frontend
   - **Environment**: Docker
   - **Region**: Same as backend
   - **Root Directory**: `frontend`
   - **Publish Directory**: `dist`

4. Environment Variables:
   ```
   VITE_API_URL=https://dns-bot-backend.render.onrender.com
   VITE_WS_URL=wss://dns-bot-backend.render.onrender.com
   ```

5. Click "Create Web Service"

## Step 3: Application URLs

After deployment:
- **Frontend**: https://dns-bot-frontend.render.onrender.com
- **Backend API**: https://dns-bot-backend.render.onrender.com
- **API Docs**: https://dns-bot-backend.render.onrender.com/docs

## Step 4: Database Migrations

If using Alembic migrations:

1. Connect to backend via SSH
2. Run: `alembic upgrade head`

Or update `build.sh` to run migrations automatically.

## Troubleshooting

### Check Logs
- Dashboard → Service → Logs tab
- View real-time logs for errors

### Common Issues

**"ModuleNotFoundError"**
- Ensure all dependencies are in `requirements.txt`
- Check Python version in Dockerfile

**"Database connection failed"**
- Verify DATABASE_URL environment variable
- Check if PostgreSQL service is running
- Use connection string from Render dashboard

**"Redis connection failed"**
- Verify REDIS_URL environment variable
- Check if Redis service is running

**"PORT already in use"**
- Render automatically assigns PORT via `$PORT` variable
- Ensure start command uses `$PORT`

**Frontend can't reach backend**
- Update VITE_API_URL to backend's actual URL
- Check CORS settings in backend config
- Verify network connectivity

### Restart Services
- Dashboard → Service → "Manual Deploy" → "Deploy"
- Or push new code to GitHub (auto-deploys)

## Scale Your Application

### Free Tier Limits
- Services spin down after 15 minutes of inactivity
- Limited to one instance per service

### Paid Plans
- Persistent services (24/7)
- Multiple instances
- Better performance

Click "Edit" on your service and select "Pro" plan.

## Monitoring & Logs

- Use Render Dashboard Logs for debugging
- Set up error tracking (Sentry, etc.)
- Monitor database usage
- Check API response times

## Next Steps

1. Set up CI/CD with GitHub Actions
2. Add monitoring and logging
3. Implement backup strategy for database
4. Set up custom domain
5. Enable SSL/HTTPS (automatic on Render)
