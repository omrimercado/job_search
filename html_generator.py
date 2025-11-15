from typing import List, Dict
from datetime import datetime

class HTMLGenerator:
    """
    Generates an HTML page displaying jobs sorted by priority.
    """

    def __init__(self, output_path: str):
        self.output_path = output_path

    def generate(self, jobs: List[Dict]) -> str:
        """
        Generate HTML page with sorted jobs.
        Returns the path to the generated file.
        """
        # Sort jobs by priority (HIGH > MED > LOW)
        priority_order = {"HIGH": 0, "MED": 1, "LOW": 2}
        sorted_jobs = sorted(jobs, key=lambda x: priority_order.get(x.get('priority', 'LOW'), 3))

        html_content = self._create_html(sorted_jobs)

        with open(self.output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"HTML page generated: {self.output_path}")
        return self.output_path

    def _create_html(self, jobs: List[Dict]) -> str:
        """Create the HTML content."""
        last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Count jobs by priority
        high_count = sum(1 for j in jobs if j.get('priority') == 'HIGH')
        med_count = sum(1 for j in jobs if j.get('priority') == 'MED')
        low_count = sum(1 for j in jobs if j.get('priority') == 'LOW')

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Job Search Results - Prioritized</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}

        .header {{
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}

        .header h1 {{
            color: #667eea;
            font-size: 2.5em;
            margin-bottom: 10px;
        }}

        .header .subtitle {{
            color: #666;
            font-size: 1.1em;
            margin-bottom: 20px;
        }}

        .stats {{
            display: flex;
            gap: 20px;
            margin-top: 20px;
        }}

        .stat-card {{
            flex: 1;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
        }}

        .stat-card.high {{
            background: #d4edda;
            border: 2px solid #28a745;
        }}

        .stat-card.med {{
            background: #fff3cd;
            border: 2px solid #ffc107;
        }}

        .stat-card.low {{
            background: #f8d7da;
            border: 2px solid #dc3545;
        }}

        .stat-card .number {{
            font-size: 2em;
            font-weight: bold;
            margin-bottom: 5px;
        }}

        .stat-card .label {{
            font-size: 0.9em;
            color: #666;
        }}

        .jobs-container {{
            display: flex;
            flex-direction: column;
            gap: 20px;
        }}

        .job-card {{
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: transform 0.2s, box-shadow 0.2s;
            border-left: 5px solid #ccc;
        }}

        .job-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        }}

        .job-card.priority-HIGH {{
            border-left-color: #28a745;
        }}

        .job-card.priority-MED {{
            border-left-color: #ffc107;
        }}

        .job-card.priority-LOW {{
            border-left-color: #dc3545;
        }}

        .job-header {{
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 15px;
        }}

        .job-title {{
            font-size: 1.5em;
            font-weight: bold;
            color: #333;
            margin-bottom: 5px;
        }}

        .job-company {{
            color: #666;
            font-size: 1.1em;
        }}

        .priority-badge {{
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.9em;
            white-space: nowrap;
        }}

        .priority-badge.HIGH {{
            background: #28a745;
            color: white;
        }}

        .priority-badge.MED {{
            background: #ffc107;
            color: #333;
        }}

        .priority-badge.LOW {{
            background: #dc3545;
            color: white;
        }}

        .job-location {{
            color: #888;
            margin-bottom: 15px;
            font-size: 0.95em;
        }}

        .job-description {{
            color: #555;
            line-height: 1.6;
            margin-bottom: 15px;
            border-left: 3px solid #e0e0e0;
            padding-left: 15px;
        }}

        .job-reasoning {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 15px;
            font-style: italic;
            color: #555;
        }}

        .job-reasoning strong {{
            color: #333;
            font-style: normal;
        }}

        .job-link {{
            display: inline-block;
            padding: 10px 20px;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 500;
            transition: background 0.2s;
        }}

        .job-link:hover {{
            background: #764ba2;
        }}

        .last-updated {{
            text-align: center;
            color: white;
            margin-top: 30px;
            font-size: 0.9em;
        }}

        .filter-buttons {{
            display: flex;
            gap: 10px;
            margin-top: 20px;
            flex-wrap: wrap;
        }}

        .filter-btn {{
            padding: 10px 20px;
            border: 2px solid #667eea;
            background: white;
            color: #667eea;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 500;
            transition: all 0.2s;
        }}

        .filter-btn:hover, .filter-btn.active {{
            background: #667eea;
            color: white;
        }}

        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 1.8em;
            }}

            .stats {{
                flex-direction: column;
            }}

            .job-header {{
                flex-direction: column;
            }}

            .priority-badge {{
                margin-top: 10px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 Job Search Results</h1>
            <div class="subtitle">Automatically prioritized based on your profile</div>

            <div class="stats">
                <div class="stat-card high">
                    <div class="number">{high_count}</div>
                    <div class="label">High Priority</div>
                </div>
                <div class="stat-card med">
                    <div class="number">{med_count}</div>
                    <div class="label">Medium Priority</div>
                </div>
                <div class="stat-card low">
                    <div class="number">{low_count}</div>
                    <div class="label">Low Priority</div>
                </div>
            </div>

            <div class="filter-buttons">
                <button class="filter-btn active" onclick="filterJobs('ALL')">All Jobs ({len(jobs)})</button>
                <button class="filter-btn" onclick="filterJobs('HIGH')">High Priority ({high_count})</button>
                <button class="filter-btn" onclick="filterJobs('MED')">Medium Priority ({med_count})</button>
                <button class="filter-btn" onclick="filterJobs('LOW')">Low Priority ({low_count})</button>
            </div>
        </div>

        <div class="jobs-container" id="jobsContainer">
"""

        # Add job cards
        for job in jobs:
            priority = job.get('priority', 'LOW')
            html += f"""
            <div class="job-card priority-{priority}" data-priority="{priority}">
                <div class="job-header">
                    <div>
                        <div class="job-title">{self._escape_html(job['title'])}</div>
                        <div class="job-company">{self._escape_html(job['company'])}</div>
                    </div>
                    <div class="priority-badge {priority}">{priority} PRIORITY</div>
                </div>

                <div class="job-location">📍 {self._escape_html(job['location'])}</div>

                <div class="job-description">
                    {self._escape_html(job['description'])}
                </div>

                <div class="job-reasoning">
                    <strong>Why this match:</strong> {self._escape_html(job.get('reasoning', 'No reasoning available'))}
                </div>

                <a href="{job['url']}" target="_blank" class="job-link">View Job on LinkedIn →</a>
            </div>
"""

        html += f"""
        </div>

        <div class="last-updated">
            Last updated: {last_updated}
        </div>
    </div>

    <script>
        function filterJobs(priority) {{
            const cards = document.querySelectorAll('.job-card');
            const buttons = document.querySelectorAll('.filter-btn');

            // Update active button
            buttons.forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');

            // Filter cards
            cards.forEach(card => {{
                if (priority === 'ALL' || card.dataset.priority === priority) {{
                    card.style.display = 'block';
                }} else {{
                    card.style.display = 'none';
                }}
            }});
        }}
    </script>
</body>
</html>
"""

        return html

    def _escape_html(self, text: str) -> str:
        """Escape HTML special characters."""
        if not text:
            return ""
        return (text
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;")
                .replace("'", "&#x27;"))
