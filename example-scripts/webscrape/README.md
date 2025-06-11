# Web Scrape Examples

This folder contains sample scripts that demonstrate simple web scraping using external dependencies.

## GitHub Trending Fetcher

Fetches names of the top trending repositories on GitHub.

### Installation

```
pip install requests beautifulsoup4
```

### Usage

Load the script in NightyScript and run:

```
<p>trending
```

## Puppeteer Screenshot

Uses Node.js and Puppeteer to capture a screenshot of any webpage. The
JavaScript code is embedded directly in the Python script, so you do not
need to keep a separate `.js` file.

### Installation

```
npm install puppeteer
```

### Usage

Load the script in NightyScript and run:

```
<p>puppshot https://example.com
```

If the screenshot fails, the command will display the captured Node.js output to
help diagnose the issue.