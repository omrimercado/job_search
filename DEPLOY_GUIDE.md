# Deployment Guide - Run Every 24 Hours in Cloud

## Option 1: GitHub Actions (FREE - Recommended) ✅

### Setup Steps (10 minutes):

#### 1. Create GitHub Repository

```bash
cd "jobs search"
git init
git add .
git commit -m "Initial commit - Job Search Automation"
```

Go to https://github.com/new and create a new repository (private recommended).

```bash
git remote add origin https://github.com/YOUR_USERNAME/job-search-automation.git
git branch -M main
git push -u origin main
```

#### 2. Add Secrets to GitHub

Go to your GitHub repository → Settings → Secrets and variables → Actions

**Add Secret:**
- Name: `ANTHROPIC_API_KEY`
- Value: `sk-ant-api03-your-key-here`

**Add Variables** (Settings → Secrets and variables → Actions → Variables):
- `YOUR_SKILLS`: React, Next.js, Angular, JavaScript, HTML, CSS, Python, FastAPI, Node.js, Java, PostgreSQL, SQL Server, MongoDB, Firebase Firestore, Redis, Vector Databases, Docker, AWS, Git, CI/CD, AI/LLM Integration
- `YOUR_EXPERIENCE_YEARS`: 0
- `YOUR_PROFILE`: Junior Full-Stack Developer with B.Sc. in Computer Science (GPU 90) from HIT...

#### 3. Done! 🎉

The workflow will automatically run every day at 11:00 AM Israel time.

**Manual Trigger:** Go to Actions tab → "Automated Job Search" → "Run workflow"

**View Results:** After each run, download `jobs_output.html` from the Artifacts section.

---

## Option 2: Google Cloud Run + Cloud Scheduler

### Cost: ~$1-3/month

### Setup Steps:

#### 1. Install Google Cloud CLI

```bash
# Download from: https://cloud.google.com/sdk/docs/install
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

#### 2. Enable Required APIs

```bash
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable cloudscheduler.googleapis.com
```

#### 3. Build and Deploy

```bash
# Build container
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/job-search

# Deploy to Cloud Run
gcloud run deploy job-search \
  --image gcr.io/YOUR_PROJECT_ID/job-search \
  --platform managed \
  --region me-west1 \
  --memory 512Mi \
  --timeout 300 \
  --set-env-vars "ANTHROPIC_API_KEY=your-key" \
  --no-allow-unauthenticated
```

#### 4. Create Scheduler

```bash
gcloud scheduler jobs create http job-search-daily \
  --location me-west1 \
  --schedule "0 11 * * *" \
  --uri "YOUR_CLOUD_RUN_URL" \
  --http-method POST \
  --oidc-service-account-email YOUR_SERVICE_ACCOUNT
```

---

## Option 3: Railway.app (Easiest Paid Option)

### Cost: ~$5/month

### Setup:

1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Add environment variables:
   - `ANTHROPIC_API_KEY`
   - `YOUR_SKILLS`
   - `YOUR_PROFILE`
   - etc.
6. Add cron job in railway.json:

```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "restartPolicyType": "ON_FAILURE"
  },
  "cron": {
    "schedule": "0 11 * * *",
    "command": "python main.py --once"
  }
}
```

---

## Option 4: AWS Lambda + EventBridge

### Cost: ~$1-2/month

More complex setup - see AWS documentation.

---

## Quick Comparison

| Service | Cost/Month | Complexity | Best For |
|---------|-----------|------------|----------|
| **GitHub Actions** | FREE | Easy | Your case! |
| Google Cloud Run | $1-3 | Medium | Scalability |
| Railway | $5-7 | Very Easy | No DevOps |
| AWS Lambda | $1-2 | Complex | Enterprise |

---

## Recommended: GitHub Actions Setup

### Why GitHub Actions?

1. **FREE** - 2000 minutes/month (your job uses ~2 minutes)
2. **Easy** - Just push code, it runs automatically
3. **Reliable** - Runs on schedule without fail
4. **Version Control** - Results saved in repository
5. **No Server** - Serverless, no maintenance

### Files Already Created:

✅ `.github/workflows/job_search.yml` - Runs every 24 hours at 11 AM Israel time

### Next Steps:

1. Create GitHub repository
2. Push your code
3. Add API key as secret
4. Done! It runs automatically every day

### Accessing Results:

**Option A - Download Artifact:**
- Go to Actions → Latest Run → Artifacts
- Download `job-search-results-X.zip`
- Open `jobs_output.html`

**Option B - Auto-commit to repo:**
- The workflow commits results back to repository
- Pull latest changes: `git pull`
- Open `jobs_output.html`

**Option C - Email notification (advanced):**
Add email step to workflow to send results to your email.

---

## Important Security Notes

⚠️ **NEVER commit your API key to the repository!**

Make sure these files are in `.gitignore`:
```
.env
jobs_output.html
__pycache__/
```

Your API key should ONLY be stored in:
- GitHub Secrets (for GitHub Actions)
- Cloud provider's secret manager
- Environment variables (never in code)

---

## Testing the Deployment

### GitHub Actions:
1. Push code to GitHub
2. Go to Actions tab
3. Click "Run workflow" to test manually
4. Check if it completes successfully
5. Download results from Artifacts

### Local Test:
```bash
python main.py --once
# Should show: High priority: X, Med priority: Y, Low priority: Z
```

---

## Monitoring & Alerts

### GitHub Actions:
- Go to Actions tab to see run history
- Enable email notifications for failed runs
- Check artifacts for daily results

### Set up Email Alerts:
Repository → Settings → Notifications → Check "Email"

---

## Cost Summary

**Your setup with GitHub Actions:**
- GitHub Actions: FREE (2000 min/month, you use ~60 min/month)
- Anthropic API: ~$9/month (50 jobs × $0.30 × 30 days)
- **Total: ~$9/month** (just the AI costs)

---

## Final Checklist

- [ ] Create GitHub repository
- [ ] Push code: `git push`
- [ ] Add `ANTHROPIC_API_KEY` secret
- [ ] Add profile variables
- [ ] Test manual run
- [ ] Verify results download
- [ ] Schedule is active (11 AM Israel time daily)

---

**Ready to deploy? Start with GitHub Actions - it's free and takes 10 minutes!**
