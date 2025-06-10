# Website Screenshot App

This example demonstrates how to capture a screenshot of a web page using Node.js and [Puppeteer](https://github.com/puppeteer/puppeteer). The app can run directly with Node or inside a Docker container.

## Requirements
- Node.js (v18 or later)
- Internet access to download page assets

## Usage

### Directly with Node.js

Install dependencies and run:

```bash
npm install
node screenshot.js <url> [output]
```

This saves a screenshot of `<url>` to `output` (default `screenshot.png`).

### With Docker

Build the container:

```bash
docker build -t website-screenshot .
```

Run it, passing the URL and optional output path:

```bash
docker run --rm -v $(pwd):/app website-screenshot "https://example.com" "out.png"
```

The screenshot will be written to `out.png` in your current directory.
