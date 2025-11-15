import requests
from bs4 import BeautifulSoup
import time
from typing import List, Dict
import json

class LinkedInJobFetcher:
    """
    Fetches job postings from LinkedIn using their public job search.
    Note: This uses the public API approach. For production, consider using official LinkedIn API.
    """

    def __init__(self, keywords: List[str], location: str, limit: int = 50):
        self.keywords = keywords
        self.location = location
        self.limit = limit
        self.base_url = "https://www.linkedin.com/jobs/search"

    def fetch_jobs(self) -> List[Dict]:
        """
        Fetch jobs from LinkedIn public job search.
        Returns a list of job dictionaries with details.
        """
        all_jobs = []

        for keyword in self.keywords:
            print(f"Fetching jobs for keyword: {keyword.strip()}")
            jobs = self._fetch_jobs_for_keyword(keyword.strip())
            all_jobs.extend(jobs)
            time.sleep(2)  # Rate limiting

        # Remove duplicates based on job URL
        unique_jobs = self._remove_duplicates(all_jobs)
        return unique_jobs[:self.limit]

    def _fetch_jobs_for_keyword(self, keyword: str) -> List[Dict]:
        """Fetch jobs for a specific keyword."""
        jobs = []

        params = {
            'keywords': keyword,
            'location': self.location,
            'f_TPR': 'r86400',  # Posted in last 24 hours (past day)
            'f_AL': 'true',  # Easy Apply filter (optional)
            'position': 1,
            'pageNum': 0,
            'sortBy': 'DD'  # Sort by date (most recent first)
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        try:
            response = requests.get(self.base_url, params=params, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Find job cards
            job_cards = soup.find_all('div', class_='base-card')

            for card in job_cards[:25]:  # Limit per keyword
                try:
                    job = self._parse_job_card(card)
                    if job:
                        jobs.append(job)
                except Exception as e:
                    print(f"Error parsing job card: {e}")
                    continue

        except Exception as e:
            print(f"Error fetching jobs for keyword '{keyword}': {e}")

        return jobs

    def _parse_job_card(self, card) -> Dict:
        """Parse a job card to extract job details."""
        try:
            # Extract job title
            title_elem = card.find('h3', class_='base-search-card__title')
            title = title_elem.text.strip() if title_elem else 'N/A'

            # Extract company name
            company_elem = card.find('h4', class_='base-search-card__subtitle')
            company = company_elem.text.strip() if company_elem else 'N/A'

            # Extract location
            location_elem = card.find('span', class_='job-search-card__location')
            location = location_elem.text.strip() if location_elem else 'N/A'

            # Extract job URL
            link_elem = card.find('a', class_='base-card__full-link')
            url = link_elem['href'] if link_elem and 'href' in link_elem.attrs else 'N/A'

            # Extract job description (if available)
            description_elem = card.find('p', class_='base-search-card__snippet')
            description = description_elem.text.strip() if description_elem else 'No description available'

            return {
                'title': title,
                'company': company,
                'location': location,
                'url': url,
                'description': description,
                'priority': None  # Will be set by LLM
            }
        except Exception as e:
            print(f"Error parsing job card details: {e}")
            return None

    def _remove_duplicates(self, jobs: List[Dict]) -> List[Dict]:
        """Remove duplicate jobs based on URL."""
        seen_urls = set()
        unique_jobs = []

        for job in jobs:
            if job['url'] not in seen_urls:
                seen_urls.add(job['url'])
                unique_jobs.append(job)

        return unique_jobs

    def fetch_job_details(self, job_url: str) -> str:
        """
        Fetch detailed job description from job URL.
        This requires more detailed scraping and may need authentication.
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        try:
            response = requests.get(job_url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Try to find job description
            description_elem = soup.find('div', class_='description__text')
            if description_elem:
                return description_elem.get_text(strip=True)

            return "Could not fetch detailed description"

        except Exception as e:
            print(f"Error fetching job details: {e}")
            return "Could not fetch detailed description"


def mock_fetch_jobs(keywords: List[str], location: str, limit: int = 50) -> List[Dict]:
    """
    Mock function for testing without actual LinkedIn scraping.
    Remove this and use LinkedInJobFetcher for production.
    """
    mock_jobs = [
        {
            'title': 'Junior Full Stack Developer',
            'company': 'Google',
            'location': 'Tel Aviv, Israel',
            'url': 'https://linkedin.com/jobs/view/123456',
            'description': 'We are seeking a Junior Full Stack Developer to join our dynamic team. Required: React, Node.js, JavaScript, HTML/CSS. Experience with Python and FastAPI is a plus. Recent graduates with strong CS fundamentals welcome. You will work on building scalable web applications and collaborate with senior engineers.',
            'priority': None
        },
        {
            'title': 'Junior Software Engineer - AI/ML Focus',
            'company': 'Microsoft Israel R&D',
            'location': 'Herzliya, Israel',
            'url': 'https://linkedin.com/jobs/view/123457',
            'description': 'Join our AI team as a Junior Software Engineer! Required: Python, JavaScript, understanding of machine learning concepts. Experience with LLMs, RAG pipelines, or vector databases is highly valued. B.Sc. in Computer Science required. Work on cutting-edge AI applications.',
            'priority': None
        },
        {
            'title': 'Junior Full Stack Developer (React + Node)',
            'company': 'Wix',
            'location': 'Tel Aviv, Israel',
            'url': 'https://linkedin.com/jobs/view/123458',
            'description': 'Entry-level Full Stack position. Must have: React, Next.js, Node.js, MongoDB or PostgreSQL. We value self-learners with passion for web development. Experience with Docker and CI/CD is a plus. Recent CS graduates encouraged to apply.',
            'priority': None
        },
        {
            'title': 'Software Engineer (Junior) - Backend',
            'company': 'Intel Israel',
            'location': 'Haifa, Israel',
            'url': 'https://linkedin.com/jobs/view/123459',
            'description': 'Junior Backend Engineer position. Required: Python or Java, SQL databases, RESTful APIs. Nice to have: FastAPI, Docker, AWS experience. Strong algorithmic thinking and problem-solving skills. B.Sc. in CS or related field required.',
            'priority': None
        },
        {
            'title': 'Junior Software Engineer - Cloud Platform',
            'company': 'Monday.com',
            'location': 'Tel Aviv, Israel',
            'url': 'https://linkedin.com/jobs/view/123460',
            'description': 'Looking for Junior Software Engineer to work on our cloud platform. Tech stack: React, Node.js, PostgreSQL, Redis, AWS, Docker. Agile environment with excellent mentorship. Experience with CI/CD pipelines is a bonus. Fresh graduates with strong portfolio welcome.',
            'priority': None
        },
        {
            'title': 'Full Stack Developer (Entry Level)',
            'company': 'JFrog',
            'location': 'Netanya, Israel',
            'url': 'https://linkedin.com/jobs/view/123461',
            'description': 'Entry-level Full Stack position. Required: JavaScript/TypeScript, React or Angular, Node.js, basic DevOps knowledge. We are looking for someone passionate about software development with good understanding of data structures and algorithms. B.Sc. in CS preferred.',
            'priority': None
        },
        {
            'title': 'Junior Software Engineer - Frontend Focus',
            'company': 'Check Point',
            'location': 'Tel Aviv, Israel',
            'url': 'https://linkedin.com/jobs/view/123462',
            'description': 'Junior Frontend Engineer role. Must have: React, JavaScript/TypeScript, HTML/CSS, Git. Experience with Next.js is a plus. Work on security products UI. Strong CS fundamentals required. Recent graduates with excellent academic record encouraged to apply.',
            'priority': None
        },
        {
            'title': 'Junior Full Stack Developer - Startup',
            'company': 'Fireblocks',
            'location': 'Tel Aviv, Israel',
            'url': 'https://linkedin.com/jobs/view/123463',
            'description': 'Join our fast-growing startup as Junior Full Stack Developer. Stack: React, Node.js, MongoDB, Firebase, Docker. We value initiative, self-learning, and problem-solving skills. Experience with real-time data and WebSockets is a bonus. B.Sc. in Computer Science required.',
            'priority': None
        },
        {
            'title': 'Software Engineer (Junior/Mid) - Python',
            'company': 'NVIDIA Israel',
            'location': 'Yokneam, Israel',
            'url': 'https://linkedin.com/jobs/view/123464',
            'description': 'Junior/Mid-level Python Engineer. Required: Python, FastAPI or Django, SQL, Git. Understanding of AI/ML concepts is highly valued. Work on AI infrastructure and tools. Strong academic background in CS required. Experience with Docker and Kubernetes is a plus.',
            'priority': None
        },
        {
            'title': 'Junior Full Stack Engineer - Enterprise',
            'company': 'SAP Labs Israel',
            'location': 'Ra\'anana, Israel',
            'url': 'https://linkedin.com/jobs/view/123465',
            'description': 'Entry-level Full Stack Engineer position. Tech: React, Angular, Node.js, Java, PostgreSQL. We seek candidates with strong OOP principles, Agile experience, and good communication skills. B.Sc. in CS or Software Engineering. AWS/GCP knowledge is advantageous.',
            'priority': None
        }
    ]

    return mock_jobs[:limit]
