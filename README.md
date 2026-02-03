# Job Board Flask Application

A Flask web application that displays jobs scraped from multiple job websites.

## Features

- Display jobs from multiple sources (OnlineJobs.ph, RemoteOK, Freelancer, Indeed, etc.)
- Filter jobs by source and category
- Search jobs by keywords
- Responsive design for mobile and desktop
- Individual job detail pages
- Direct links to apply on original websites

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Make sure you have scraped jobs data:
```bash
cd ..
python run_scrapers.py
```

2. Start the Flask server:
```bash
python app.py
```

3. Open your browser and visit:
```
http://localhost:5000
```

## Project Structure

```
jobs_flask/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── static/
│   └── style.css      # CSS styling
└── templates/
    ├── base.html      # Base template
    ├── index.html     # Job listings page
    ├── job_detail.html # Individual job detail page
    └── refresh.html   # Instructions for refreshing jobs
```

## Refreshing Jobs

To get fresh job listings:

1. Run the scraper from parent directory:
```bash
cd ..
python run_scrapers.py
cd jobs_flask
```

2. Copy the updated jobs to jobs_flask:
   - **Windows**: Double-click `update_jobs.bat`
   - **Manual**: Copy `scraped_jobs.json` from parent folder to jobs_flask folder

3. Refresh the browser - no need to restart Flask server

## API Endpoints

- `GET /` - Main job listings page with filters
- `GET /job/<id>` - Individual job detail page
- `GET /api/jobs` - JSON API for jobs data
- `GET /refresh` - Information page about refreshing jobs

## Filters

- **Search** - Search by job title or description
- **Source** - Filter by job source (OnlineJobs.ph, RemoteOK, etc.)
- **Category** - Filter by job category/type
