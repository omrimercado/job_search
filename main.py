import schedule
import time
import sys
import os
from datetime import datetime

# Fix Windows console encoding issue
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
    os.environ['PYTHONIOENCODING'] = 'utf-8'

from config import Config
from linkedin_fetcher import LinkedInJobFetcher, mock_fetch_jobs
from job_scorer import JobScorer, mock_score_jobs
from html_generator import HTMLGenerator

def run_job_search():
    """
    Main function to fetch, score, and generate HTML for jobs.
    """
    print(f"\n{'='*60}")
    print(f"Starting job search at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    try:
        # Step 1: Fetch jobs from LinkedIn
        print("Step 1: Fetching jobs from LinkedIn...")
        print(f"Keywords: {Config.JOB_KEYWORDS}")
        print(f"Location: {Config.JOB_LOCATION}")
        print(f"Limit: {Config.JOB_LIMIT}\n")

        # Real LinkedIn fetcher
        fetcher = LinkedInJobFetcher(
            keywords=Config.JOB_KEYWORDS,
            location=Config.JOB_LOCATION,
            limit=Config.JOB_LIMIT
        )
        jobs = fetcher.fetch_jobs()

        # Fallback to mock data if no real jobs found
        if not jobs:
            print("⚠ No jobs found from LinkedIn. Using mock data as fallback...")
            jobs = mock_fetch_jobs(
                keywords=Config.JOB_KEYWORDS,
                location=Config.JOB_LOCATION,
                limit=Config.JOB_LIMIT
            )

        print(f"✓ Fetched {len(jobs)} jobs\n")

        if not jobs:
            print("No jobs found. Exiting...")
            return

        # Step 2: Score jobs using LLM
        print("Step 2: Scoring jobs with LLM...")

        if Config.ANTHROPIC_API_KEY and Config.ANTHROPIC_API_KEY != 'your_api_key_here':
            scorer = JobScorer(
                api_key=Config.ANTHROPIC_API_KEY,
                user_profile=Config.YOUR_PROFILE,
                user_skills=Config.YOUR_SKILLS,
                user_experience=Config.YOUR_EXPERIENCE_YEARS
            )
            scored_jobs = scorer.score_jobs(jobs)
        else:
            print("⚠ No API key found. Using mock scoring...")
            scored_jobs = mock_score_jobs(jobs, Config.YOUR_PROFILE)

        print(f"✓ Scored {len(scored_jobs)} jobs\n")

        # Step 3: Generate HTML page
        print("Step 3: Generating HTML page...")
        generator = HTMLGenerator(Config.OUTPUT_HTML_PATH)
        output_path = generator.generate(scored_jobs)
        print(f"✓ HTML page generated at: {output_path}\n")

        # Print summary
        high_count = sum(1 for j in scored_jobs if j.get('priority') == 'HIGH')
        med_count = sum(1 for j in scored_jobs if j.get('priority') == 'MED')
        low_count = sum(1 for j in scored_jobs if j.get('priority') == 'LOW')

        print(f"\n{'='*60}")
        print("Summary:")
        print(f"  Total jobs: {len(scored_jobs)}")
        print(f"  High priority: {high_count}")
        print(f"  Medium priority: {med_count}")
        print(f"  Low priority: {low_count}")
        print(f"{'='*60}\n")

    except Exception as e:
        print(f"❌ Error during job search: {e}")
        import traceback
        traceback.print_exc()


def run_scheduled():
    """
    Run the job search on a schedule (every 24 hours).
    """
    print("🤖 Job Search Automation Started")
    print(f"Will run every {Config.UPDATE_INTERVAL_HOURS} hours")
    print("Press Ctrl+C to stop\n")

    # Run immediately on start
    run_job_search()

    # Schedule to run every 24 hours
    schedule.every(Config.UPDATE_INTERVAL_HOURS).hours.do(run_job_search)

    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute


def run_once():
    """
    Run the job search once and exit.
    """
    run_job_search()


if __name__ == "__main__":
    import sys

    # Check command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "--once":
        # Run once and exit
        run_once()
    elif len(sys.argv) > 1 and sys.argv[1] == "--schedule":
        # Run on schedule
        run_scheduled()
    else:
        # Default: run once
        print("Usage:")
        print("  python main.py --once      # Run once and exit")
        print("  python main.py --schedule  # Run every 24 hours")
        print("\nRunning once by default...\n")
        run_once()
