const puppeteer = require('puppeteer');

(async () => {
  const url = process.argv[2];
  const output = process.argv[3] || 'screenshot.png';
  if (!url) {
    console.error('Usage: node screenshot.js <url> [output]');
    process.exit(1);
  }

  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  const page = await browser.newPage();
  await page.goto(url, { waitUntil: 'networkidle2' });
  await page.screenshot({ path: output, fullPage: true });
  await browser.close();
})();
