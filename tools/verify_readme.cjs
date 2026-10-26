/* Maintainer check: requires Playwright and an installed Microsoft Edge. */
const { chromium } = require('playwright');
const fs = require('node:fs/promises');
const path = require('node:path');
const { pathToFileURL } = require('node:url');

async function main() {
  const root = path.resolve(__dirname, '..');
  const out = path.join(root, 'output', 'qa');
  await fs.mkdir(out, { recursive: true });
  const browser = await chromium.launch({
    executablePath: process.env.EDGE_PATH || 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
    headless: true,
  });
  try {
    const page = await browser.newPage({ viewport: { width: 1440, height: 1080 } });
    const errors = [];
    const externalRequests = [];
    page.on('pageerror', error => errors.push(String(error)));
    page.on('request', request => { if (/^https?:/.test(request.url())) externalRequests.push(request.url()); });
    await page.goto(pathToFileURL(path.join(root, 'assignment-template', 'README.html')).href);
    const results = await page.evaluate(() => ({
      language: document.documentElement.lang,
      direction: getComputedStyle(document.documentElement).direction,
      codeDirection: getComputedStyle(document.querySelector('pre')).direction,
      themeButtons: document.querySelectorAll('[data-theme]').length,
      codeBlocks: document.querySelectorAll('pre').length,
      copyButtons: document.querySelectorAll('.copy').length,
      missingAnchors: [...document.querySelectorAll('.toc a')].filter(a => !document.getElementById(decodeURIComponent(a.hash.slice(1)))).map(a => a.hash),
      overflow: document.documentElement.scrollWidth > innerWidth,
    }));
    if (results.direction !== 'rtl' || results.language !== 'fa' || results.codeDirection !== 'ltr') throw new Error('Wrong text direction');
    if (results.themeButtons !== 5 || results.codeBlocks !== results.copyButtons) throw new Error('Missing theme or copy controls');
    if (results.missingAnchors.length || results.overflow) throw new Error('Desktop navigation/overflow issue');
    results.palettes = {};
    for (const theme of ['warm', 'blue', 'green', 'plum', 'teal']) {
      await page.locator(`[data-theme="${theme}"]`).click();
      const state = await page.evaluate(() => ({
        setting: document.getElementById('theme-setting').textContent,
        background: getComputedStyle(document.querySelector('.preview-title')).backgroundColor,
        selected: document.querySelector('[aria-pressed=true]').dataset.theme,
      }));
      if (state.selected !== theme || !state.setting.endsWith(`{${theme}}`)) throw new Error(`Theme switch failed: ${theme}`);
      results.palettes[theme] = state;
    }
    await page.locator('[data-theme="warm"]').click();
    await page.screenshot({ path: path.join(out, 'readme-desktop.png') });
    await page.setViewportSize({ width: 390, height: 844 });
    await page.evaluate(() => scrollTo(0, 0));
    results.mobileOverflow = await page.evaluate(() => document.documentElement.scrollWidth > innerWidth);
    if (results.mobileOverflow) throw new Error('Mobile horizontal overflow');
    await page.screenshot({ path: path.join(out, 'readme-mobile.png') });
    results.externalRequests = externalRequests;
    results.errors = errors;
    if (errors.length || externalRequests.length) throw new Error('Unexpected browser errors or network requests');
    await fs.writeFile(path.join(out, 'readme-check.json'), JSON.stringify(results, null, 2) + '\n');
    console.log(JSON.stringify(results, null, 2));
  } finally { await browser.close(); }
}
main().catch(error => { console.error(error); process.exitCode = 1; });
