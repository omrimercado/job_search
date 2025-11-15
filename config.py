import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

    # LinkedIn Credentials
    LINKEDIN_EMAIL = os.getenv('LINKEDIN_EMAIL')
    LINKEDIN_PASSWORD = os.getenv('LINKEDIN_PASSWORD')

    # Job Search Parameters
    JOB_KEYWORDS = os.getenv('JOB_KEYWORDS', 'software engineer').split(',')
    JOB_LOCATION = os.getenv('JOB_LOCATION', 'United States')
    JOB_LIMIT = int(os.getenv('JOB_LIMIT', '50'))

    # User Profile for Matching
    YOUR_SKILLS = os.getenv('YOUR_SKILLS', '')
    YOUR_EXPERIENCE_YEARS = os.getenv('YOUR_EXPERIENCE_YEARS', '0')
    YOUR_PROFILE = os.getenv('YOUR_PROFILE', '')

    # Output
    OUTPUT_HTML_PATH = 'jobs_output.html'

    # Scheduling
    UPDATE_INTERVAL_HOURS = 24
