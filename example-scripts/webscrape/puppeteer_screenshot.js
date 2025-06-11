const fs = require('fs');
const puppeteer = require('puppeteer');

(async () => {
  const [url, output] = process.argv.slice(2);
  if (!url || !output) {
    console.error('Usage: node puppeteer_screenshot.js <url> <output>');
    process.exit(1);
  }
  const browser = await puppeteer.launch();
  try {
    const page = await browser.newPage();
    await page.goto(url, { waitUntil: 'networkidle2' });
    await page.screenshot({ path: output, fullPage: true });
  } catch (err) {
    console.error(err.toString());
    process.exit(1);
  } finally {
    await browser.close();
  }
})();
