"""
Flask Job Board - Display scraped jobs from multiple sources
"""
from flask import Flask, render_template, request, jsonify
import json
import re
import math
import os
from html import unescape
from pathlib import Path
from datetime import datetime

app = Flask(__name__)

# Path to scraped jobs JSON (inside jobs_flask folder)
JOBS_FILE = Path(__file__).parent / 'scraped_jobs.json'

JOBS_PER_PAGE = 20

# Work arrangement keywords
ARRANGEMENT_KEYWORDS = {
    'remote': ['remote', 'work from home', 'wfh', 'anywhere'],
    'hybrid': ['hybrid'],
    'onsite': ['onsite', 'on-site', 'on site', 'in-office', 'in office'],
}

# Job type keywords
TYPE_KEYWORDS = {
    'full-time': ['full-time', 'full time', 'fulltime'],
    'part-time': ['part-time', 'part time', 'parttime'],
    'contract': ['contract'],
    'freelance': ['freelance', 'gig'],
}


def detect_arrangement(job):
    """Detect work arrangement from job fields."""
    text = ' '.join([
        job.get('location') or '',
        job.get('title') or '',
        job.get('category') or '',
        job.get('type') or '',
    ]).lower()
    for arrangement, keywords in ARRANGEMENT_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                return arrangement
    return ''


def detect_job_type(job):
    """Detect job type from job fields."""
    text = ' '.join([
        job.get('category') or '',
        job.get('type') or '',
        job.get('title') or '',
    ]).lower()
    for jtype, keywords in TYPE_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                return jtype
    return ''


def parse_date(job):
    """Parse posted_date into a naive datetime for sorting. Returns None if unparseable."""
    raw = job.get('posted_date') or job.get('date_posted') or ''
    if not raw:
        return None
    try:
        dt = datetime.fromisoformat(raw)
        # Strip timezone info for consistent comparison
        return dt.replace(tzinfo=None)
    except (ValueError, TypeError):
        pass
    try:
        return datetime.strptime(raw, '%Y-%m-%d')
    except (ValueError, TypeError):
        return None


def load_jobs():
    """Load jobs from JSON file"""
    try:
        with open(JOBS_FILE, 'r', encoding='utf-8') as f:
            jobs = json.load(f)
            for idx, job in enumerate(jobs):
                normalize_job_text(job)
                job['id'] = idx
                job['_arrangement'] = detect_arrangement(job)
                job['_job_type'] = detect_job_type(job)
                job['_parsed_date'] = parse_date(job)
            return jobs
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


def get_unique_sources(jobs):
    """Get unique job sources for filtering"""
    sources = set()
    for job in jobs:
        if job.get('source'):
            sources.add(job.get('source'))
    return sorted(list(sources))


def get_unique_categories(jobs):
    """Get unique categories for filtering"""
    categories = set()
    for job in jobs:
        if job.get('category'):
            categories.add(job.get('category'))
        if job.get('type'):
            categories.add(job.get('type'))
    return sorted(list(categories))


_TAG_RE = re.compile(r"<[^>]+>")
_BR_RE = re.compile(r"<\\s*br\\s*/?\\s*>", re.IGNORECASE)


def clean_text(value):
    """Strip HTML tags and normalize whitespace."""
    if value is None:
        return ""
    if not isinstance(value, str):
        value = str(value)
    text = _BR_RE.sub("\n", value)
    text = unescape(text)
    text = _TAG_RE.sub(" ", text)
    lines = [" ".join(line.split()) for line in text.splitlines()]
    return "\n".join([line for line in lines if line])


def normalize_job_text(job):
    """Normalize job text fields to avoid None and HTML artifacts."""
    for key in ("title", "description", "job_description", "company", "location", "salary", "type", "category"):
        if key in job:
            job[key] = clean_text(job.get(key))


def apply_filters(jobs, source_filter='', category_filter='', search_query='',
                  arrangement_filter='', job_type_filter='', sort_by=''):
    """Apply all filters and sorting to a job list."""
    filtered = jobs

    if source_filter:
        filtered = [j for j in filtered if j.get('source', '') == source_filter]

    if category_filter:
        filtered = [j for j in filtered
                    if j.get('category', '') == category_filter or j.get('type', '') == category_filter]

    if arrangement_filter:
        filtered = [j for j in filtered if j.get('_arrangement') == arrangement_filter]

    if job_type_filter:
        filtered = [j for j in filtered if j.get('_job_type') == job_type_filter]

    if search_query:
        q = search_query.lower()
        filtered = [j for j in filtered
                    if q in (j.get('title') or '').lower()
                    or q in (j.get('description') or '').lower()
                    or q in (j.get('job_description') or '').lower()]

    # Sorting
    if sort_by == 'newest':
        filtered.sort(key=lambda j: j.get('_parsed_date') or datetime.min, reverse=True)
    elif sort_by == 'oldest':
        filtered.sort(key=lambda j: j.get('_parsed_date') or datetime.min)

    return filtered


@app.route('/')
def index():
    """Main page - display all jobs with filters and pagination"""
    jobs = load_jobs()

    source_filter = request.args.get('source', '')
    category_filter = request.args.get('category', '')
    search_query = request.args.get('search', '')
    arrangement_filter = request.args.get('arrangement', '')
    job_type_filter = request.args.get('job_type', '')
    sort_by = request.args.get('sort', '')

    filtered_jobs = apply_filters(jobs, source_filter, category_filter, search_query,
                                  arrangement_filter, job_type_filter, sort_by)

    # Pagination
    total_filtered = len(filtered_jobs)
    total_pages = max(1, math.ceil(total_filtered / JOBS_PER_PAGE))
    current_page = request.args.get('page', 1, type=int)
    current_page = max(1, min(current_page, total_pages))
    start = (current_page - 1) * JOBS_PER_PAGE
    paginated_jobs = filtered_jobs[start:start + JOBS_PER_PAGE]

    sources = get_unique_sources(jobs)
    categories = get_unique_categories(jobs)

    return render_template('index.html',
                         jobs=paginated_jobs,
                         total_jobs=len(jobs),
                         filtered_count=total_filtered,
                         sources=sources,
                         categories=categories,
                         current_source=source_filter,
                         current_category=category_filter,
                         search_query=search_query,
                         current_arrangement=arrangement_filter,
                         current_job_type=job_type_filter,
                         current_sort=sort_by,
                         current_page=current_page,
                         total_pages=total_pages)


@app.route('/job/<int:job_id>')
def job_detail(job_id):
    """Job detail page"""
    jobs = load_jobs()
    if 0 <= job_id < len(jobs):
        return render_template('job_detail.html', job=jobs[job_id])
    return "Job not found", 404


@app.route('/api/job/<int:job_id>')
def api_job_detail(job_id):
    """API endpoint to get a single job as JSON"""
    jobs = load_jobs()
    if 0 <= job_id < len(jobs):
        return jsonify(jobs[job_id])
    return jsonify({'error': 'Job not found'}), 404


@app.route('/api/jobs')
def api_jobs():
    """API endpoint to get jobs as JSON"""
    jobs = load_jobs()

    filtered = apply_filters(
        jobs,
        source_filter=request.args.get('source', ''),
        category_filter=request.args.get('category', ''),
        search_query=request.args.get('search', ''),
        arrangement_filter=request.args.get('arrangement', ''),
        job_type_filter=request.args.get('job_type', ''),
        sort_by=request.args.get('sort', ''),
    )

    return jsonify({
        'total': len(jobs),
        'filtered': len(filtered),
        'jobs': filtered
    })


@app.route('/refresh')
def refresh():
    """Information page about refreshing jobs"""
    last_updated = None
    if JOBS_FILE.exists():
        mod_time = os.path.getmtime(JOBS_FILE)
        last_updated = datetime.fromtimestamp(mod_time).strftime('%B %d, %Y at %I:%M %p')
    jobs = load_jobs()
    return render_template('refresh.html', last_updated=last_updated, total_jobs=len(jobs))


@app.template_filter('truncate_words')
def truncate_words(text, length=50):
    """Truncate text to specified number of words"""
    if not text:
        return ""
    words = text.split()
    if len(words) <= length:
        return text
    return ' '.join(words[:length]) + '...'


if __name__ == '__main__':
    print("=" * 60)
    print("JOB BOARD FLASK APP")
    print("=" * 60)
    print(f"Jobs file: {JOBS_FILE}")
    print(f"Total jobs available: {len(load_jobs())}")
    print("\nStarting Flask server...")
    print("Visit: http://localhost:5000")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
