# template-scraper
A template repository containing various scripts and notebooks for testing web scraping techniques and analyzing server responses

# requests
In here are different scripts that use the python request library to test a given website.

# httpx
All of the scripts that are in request are mirrored here except that they use `httpx` as a library

# robots
testing script to analyse the `robots.txt` of a website

# `performanceAnalyser.py`

Analyze website performance: status code, page size, load time, redirects, and headers.

## Usage
```bash
uv run performanceAnalyser.py https://example.com
uv run performanceAnalyser.py https://example.com --user-agent "CustomAgent/1.0"
```
