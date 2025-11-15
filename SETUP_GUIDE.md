# Setup Guide for Omri's Job Search Automation

## Current Status
✅ Project structure created
✅ All modules implemented
✅ Successfully tested with mock data
✅ HTML dashboard generated at `jobs_output.html`

## Your Configuration
The system is configured to search for:
- **Job Titles**: Junior Software Engineer, Junior Full Stack Developer
- **Location**: Israel
- **Time Filter**: Last 24 hours
- **Your Profile**: Junior Full-Stack Developer from HIT with AI/ML focus

## Next Steps to Use Real Data

### 1. Get Anthropic API Key (Required for AI Scoring)

1. Go to [https://console.anthropic.com/](https://console.anthropic.com/)
2. Sign up or log in
3. Go to API Keys section
4. Create a new API key
5. Copy the key (starts with `sk-ant-...`)

### 2. Update .env File

Open `.env` file and replace:
```
ANTHROPIC_API_KEY=your_api_key_here
```

With your actual key:
```
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxx
```

### 3. Run with Real AI Scoring

```bash
python main.py --once
```

This will:
- Fetch jobs (currently using mock data for testing)
- Score each job using Claude AI based on your resume
- Generate prioritized HTML dashboard

### 4. Enable Real LinkedIn Scraping (Optional)

Currently, the app uses mock data for testing. To enable real LinkedIn scraping:

#### Edit `main.py` line 32-39:

Change from:
```python
# Using mock data for now
jobs = mock_fetch_jobs(
    keywords=Config.JOB_KEYWORDS,
    location=Config.JOB_LOCATION,
    limit=Config.JOB_LIMIT
)
```

To:
```python
# Real LinkedIn fetcher
fetcher = LinkedInJobFetcher(
    keywords=Config.JOB_KEYWORDS,
    location=Config.JOB_LOCATION,
    limit=Config.JOB_LIMIT
)
jobs = fetcher.fetch_jobs()
```

**Note**: LinkedIn actively blocks scrapers. For production use, consider:
- Using LinkedIn's official API (requires partnership)
- Implementing proxy rotation
- Adding delays between requests
- Using alternative job sources (Indeed, Glassdoor, etc.)

## Usage Options

### Option 1: Run Once (Manual)
```bash
python main.py --once
```
- Fetches jobs now
- Generates HTML
- Exits

### Option 2: Run on Schedule (Automated)
```bash
python main.py --schedule
```
- Runs immediately
- Then runs every 24 hours automatically
- Keeps running until you stop it (Ctrl+C)

### Option 3: Use with Real API but Mock Jobs (Recommended for Testing)
1. Add your Anthropic API key to `.env`
2. Keep mock_fetch_jobs in main.py
3. Run: `python main.py --once`

This way you can test the AI scoring without worrying about LinkedIn blocking.

## Viewing Results

After running, open `jobs_output.html` in your browser. You'll see:

- **Summary statistics** (HIGH/MED/LOW counts)
- **Filter buttons** to show only specific priorities
- **Job cards** sorted by priority with:
  - Job title and company
  - Location
  - Description
  - **AI reasoning** for the priority level
  - Direct link to LinkedIn

## Customization

### Change Job Search Terms
Edit `.env`:
```
JOB_KEYWORDS=Junior Software Engineer,Junior Full Stack Developer,Entry Level Developer
JOB_LOCATION=Tel Aviv, Israel
JOB_LIMIT=100
```

### Update Your Profile
Already configured based on your resume! But you can modify in `.env`:
```
YOUR_SKILLS=React, Next.js, Angular, JavaScript, Python, FastAPI, ...
YOUR_EXPERIENCE_YEARS=2
YOUR_PROFILE=Your professional summary...
```

### Customize HTML Design
Edit `html_generator.py` to change:
- Colors
- Layout
- Fonts
- Additional information to display

## Cloud Deployment (24/7 Automation)

### Using Docker (Easiest)

1. Make sure Docker is installed
2. Update `.env` with your API key
3. Run:
```bash
docker-compose up -d
```

The service will now run 24/7 and update every 24 hours.

View logs:
```bash
docker logs -f job-search-automation
```

Stop:
```bash
docker-compose down
```

### Using AWS/GCP
Follow instructions in `README.md` for cloud deployment.

## Cost Estimation

### Anthropic API Costs (Claude 3.5 Sonnet):
- Input: ~$3 per million tokens
- Output: ~$15 per million tokens

**Estimated cost per run** (50 jobs):
- ~50,000 input tokens (~$0.15)
- ~10,000 output tokens (~$0.15)
- **Total: ~$0.30 per run**
- **Monthly (daily runs): ~$9**

You can reduce costs by:
- Limiting jobs to 25 instead of 50
- Running every 2-3 days instead of daily
- Using Claude Haiku (cheaper model)

## Troubleshooting

### "No API key found"
- Check `.env` file has correct API key
- Make sure there are no spaces around the `=` sign
- Restart the application after changing `.env`

### LinkedIn Scraping Issues
- LinkedIn may block automated access
- Try using mock data for testing
- Consider using official APIs for production

### HTML Not Updating
- Check if script is running: `ps aux | grep python` (Linux/Mac) or Task Manager (Windows)
- Check logs for errors
- Verify file permissions

## Support

For issues:
1. Check error messages in terminal
2. Review `README.md` for detailed documentation
3. Check configuration in `.env`

## Quick Test Checklist

- [x] Dependencies installed (`pip install -r requirements.txt`)
- [x] Configuration set in `.env`
- [ ] Anthropic API key added (for real AI scoring)
- [x] First test run completed (`python main.py --once`)
- [x] HTML file generated and viewable
- [ ] Ready for production use

---

**Current Status**: System is working with mock data! Add your Anthropic API key to enable real AI-powered job matching.
