from anthropic import Anthropic
from typing import List, Dict
import json
from config import Config

class JobScorer:
    """
    Uses Claude (Anthropic) LLM to score jobs based on user profile and requirements.
    """

    def __init__(self, api_key: str, user_profile: str, user_skills: str, user_experience: str):
        self.client = Anthropic(api_key=api_key)
        self.user_profile = user_profile
        self.user_skills = user_skills
        self.user_experience = user_experience

    def score_jobs(self, jobs: List[Dict]) -> List[Dict]:
        """
        Score all jobs and assign priority (HIGH, MED, LOW).
        """
        print(f"Scoring {len(jobs)} jobs using Claude LLM...")

        for i, job in enumerate(jobs):
            print(f"Scoring job {i+1}/{len(jobs)}: {job['title']} at {job['company']}")
            priority, reasoning = self._score_single_job(job)
            job['priority'] = priority
            job['reasoning'] = reasoning

        return jobs

    def _score_single_job(self, job: Dict) -> tuple[str, str]:
        """
        Score a single job and return priority and reasoning.
        """
        prompt = self._create_scoring_prompt(job)

        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=1000,
                temperature=0,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            response_text = message.content[0].text
            priority, reasoning = self._parse_llm_response(response_text)

            return priority, reasoning

        except Exception as e:
            print(f"Error scoring job: {e}")
            return "LOW", f"Error occurred during scoring: {str(e)}"

    def _create_scoring_prompt(self, job: Dict) -> str:
        """
        Create a prompt for the LLM to score the job.
        """
        prompt = f"""You are a career advisor helping evaluate job opportunities.

USER PROFILE:
- Skills: {self.user_skills}
- Experience: {self.user_experience} years
- Profile: {self.user_profile}

JOB POSTING:
- Title: {job['title']}
- Company: {job['company']}
- Location: {job['location']}
- Description: {job['description']}

Analyze how well this job matches the user's profile. Consider:
1. Skills match (required vs. user's skills)
2. Experience level fit
3. Career growth potential
4. Job responsibilities alignment

Provide your assessment in the following format:
PRIORITY: [HIGH/MED/LOW]
REASONING: [2-3 sentences explaining why]

Guidelines:
- HIGH: Excellent match (80%+ skills match, experience fits, strong alignment)
- MED: Good match (50-79% skills match, reasonable fit with some gaps)
- LOW: Poor match (<50% skills match, significant gaps, or misalignment)

Your response:"""

        return prompt

    def _parse_llm_response(self, response: str) -> tuple[str, str]:
        """
        Parse the LLM response to extract priority and reasoning.
        """
        try:
            lines = response.strip().split('\n')
            priority = "LOW"
            reasoning = "No reasoning provided"

            for line in lines:
                if line.startswith("PRIORITY:"):
                    priority_text = line.replace("PRIORITY:", "").strip()
                    # Extract HIGH, MED, or LOW
                    if "HIGH" in priority_text.upper():
                        priority = "HIGH"
                    elif "MED" in priority_text.upper():
                        priority = "MED"
                    else:
                        priority = "LOW"

                elif line.startswith("REASONING:"):
                    reasoning = line.replace("REASONING:", "").strip()

            # If reasoning spans multiple lines, capture them
            if "REASONING:" in response:
                reasoning_start = response.index("REASONING:") + len("REASONING:")
                reasoning = response[reasoning_start:].strip()

            return priority, reasoning

        except Exception as e:
            print(f"Error parsing LLM response: {e}")
            return "LOW", "Could not parse LLM response"

    def batch_score_jobs(self, jobs: List[Dict], batch_size: int = 5) -> List[Dict]:
        """
        Score jobs in batches for efficiency (optional optimization).
        """
        # For now, we'll score individually, but this can be optimized
        # to send multiple jobs in one prompt
        return self.score_jobs(jobs)


def mock_score_jobs(jobs: List[Dict], user_profile: str) -> List[Dict]:
    """
    Mock scorer for testing without API calls.
    """
    import random

    priorities = ["HIGH", "MED", "LOW"]
    reasonings = {
        "HIGH": "Excellent match with your skills and experience. Strong alignment with career goals.",
        "MED": "Good match with some skill gaps. Reasonable fit for your background.",
        "LOW": "Limited match with your profile. Significant gaps in required skills."
    }

    for job in jobs:
        priority = random.choice(priorities)
        job['priority'] = priority
        job['reasoning'] = reasonings[priority]

    return jobs
