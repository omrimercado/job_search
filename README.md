# Automated Job Search Service

An intelligent job search automation service that fetches LinkedIn job postings, uses AI (Claude LLM) to prioritize them based on your profile, and generates a beautiful HTML dashboard updated every 24 hours.

## Features

- 🔍 **Automated Job Fetching**: Scrapes LinkedIn for relevant job postings
- 🤖 **AI-Powered Prioritization**: Uses Claude LLM to score jobs (HIGH/MED/LOW) based on your skills and experience
- 📊 **Beautiful Dashboard**: Generates a responsive HTML page with filtering capabilities
- ⏰ **Automated Updates**: Runs every 24 hours to keep your job list fresh
- ☁️ **Cloud-Ready**: Includes configurations for AWS, GCP, and Docker deployment

## Quick Start

### 1. Installation

```bash
# Clone or download this repository
cd "jobs search"

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Edit `.env` with your details:

```env
ANTHROPIC_API_KEY=your_anthropic_api_key
JOB_KEYWORDS=python developer, software engineer
JOB_LOCATION=United States
JOB_LIMIT=50
YOUR_SKILLS=Python, JavaScript, React, AWS, Docker
YOUR_EXPERIENCE_YEARS=5
YOUR_PROFILE=Experienced full-stack developer with focus on Python and cloud technologies
```

### 3. Run the Service

**Run once:**
```bash
python main.py --once
```

**Run on schedule (every 24 hours):**
```bash
python main.py --schedule
```

The HTML dashboard will be generated at `jobs_output.html`. Open it in your browser to see your prioritized jobs!

## Project Structure

```
jobs-search/
├── main.py                 # Main application entry point
├── config.py              # Configuration management
├── linkedin_fetcher.py    # LinkedIn job scraping module
├── job_scorer.py          # LLM-based job scoring
├── html_generator.py      # HTML dashboard generator
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── Dockerfile            # Docker container configuration
├── docker-compose.yml    # Docker Compose setup
└── README.md            # This file
```

## Cloud Deployment

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker logs -f job-search-automation

# Stop
docker-compose down
```

### AWS EC2 Deployment

1. Launch an EC2 instance (Ubuntu/Amazon Linux)
2. Install Docker on the instance
3. Update `deploy-aws.sh` with your EC2 details
4. Run: `bash deploy-aws.sh`

### Google Cloud Run Deployment

1. Install Google Cloud SDK
2. Update `deploy-gcp.sh` with your project details
3. Run: `bash deploy-gcp.sh`

### Heroku Deployment

```bash
# Login to Heroku
heroku login

# Create app
heroku create your-job-search-app

# Set environment variables
heroku config:set ANTHROPIC_API_KEY=your_key
heroku config:set JOB_KEYWORDS="python developer"
# ... set other variables

# Deploy
git push heroku main
```

## Configuration Options

### Job Search Parameters

- `JOB_KEYWORDS`: Comma-separated list of job titles/keywords to search for
- `JOB_LOCATION`: Geographic location for job search
- `JOB_LIMIT`: Maximum number of jobs to fetch (default: 50)

### User Profile (for AI matching)

- `YOUR_SKILLS`: Your technical skills (comma-separated)
- `YOUR_EXPERIENCE_YEARS`: Years of professional experience
- `YOUR_PROFILE`: Brief description of your background and career goals

### API Keys

- `ANTHROPIC_API_KEY`: Get your API key from [Anthropic Console](https://console.anthropic.com/)

## How It Works

1. **Fetch Jobs**: The service fetches job postings from LinkedIn based on your keywords and location
2. **AI Scoring**: Each job is analyzed by Claude LLM, which compares:
   - Required skills vs. your skills
   - Experience level match
   - Career alignment
   - Growth potential
3. **Prioritization**: Jobs are assigned HIGH/MED/LOW priority
4. **HTML Generation**: A beautiful, filterable dashboard is created
5. **Scheduling**: The process repeats every 24 hours

## Priority Levels

- **HIGH**: 80%+ skills match, excellent fit for your profile
- **MED**: 50-79% skills match, reasonable fit with some gaps
- **LOW**: <50% skills match, significant gaps or misalignment

## Troubleshooting

### LinkedIn Scraping Issues

LinkedIn actively blocks scrapers. Solutions:
- Use official LinkedIn API (requires partnership)
- Implement delays and user-agent rotation
- Consider using the mock data mode for testing

### API Rate Limits

Claude API has rate limits. To manage:
- Reduce `JOB_LIMIT` in `.env`
- Add delays between API calls in `job_scorer.py`
- Upgrade your Anthropic API plan

### HTML Not Updating

- Check file permissions
- Verify the script is running: `ps aux | grep python`
- Check logs for errors

## Development

### Testing with Mock Data

The application includes mock data for testing without API calls:

```python
# In main.py, the mock mode is enabled by default
jobs = mock_fetch_jobs(...)  # Mock LinkedIn data
scored_jobs = mock_score_jobs(...)  # Mock AI scoring
```

### Customizing the HTML

Edit `html_generator.py` to customize:
- Color scheme
- Layout
- Additional job fields
- Filtering options

### Adding Job Sources

Extend `linkedin_fetcher.py` or create new fetcher modules for:
- Indeed
- Glassdoor
- Company career pages
- Job boards

## Contributing

Feel free to submit issues, fork the repository, and create pull requests!

## License

MIT License - feel free to use this for personal or commercial projects.

## Disclaimer

This tool is for personal use only. Respect LinkedIn's Terms of Service and robots.txt. Consider using official APIs for production use.

## Support

For issues or questions, please open a GitHub issue or contact the maintainer.

---

**Happy Job Hunting! 🎯**
