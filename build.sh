#!/usr/bin/env bash
# Render build script

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Initializing scraped_jobs.json if it doesn't exist..."
if [ ! -f scraped_jobs.json ]; then
    echo "[]" > scraped_jobs.json
    echo "Created empty scraped_jobs.json"
else
    echo "scraped_jobs.json already exists"
fi

echo "Build complete!"
